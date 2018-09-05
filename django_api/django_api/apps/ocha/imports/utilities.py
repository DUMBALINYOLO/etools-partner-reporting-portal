import logging
from time import sleep

import base64
import requests
from django.core.cache import cache
from django.conf import settings
from requests import RequestException
from requests.status_codes import codes

from cluster.models import Cluster, ClusterObjective
from core.common import EXTERNAL_DATA_SOURCES
from core.models import Country, GatewayType, Location
from indicator.models import Reportable, IndicatorBlueprint, Disaggregation, DisaggregationValue, ReportableLocationGoal
from ocha.constants import HPC_V2_ROOT_URL
from ocha.utilities import get_dict_from_list_by_key, convert_to_json_ratio_value

logger = logging.getLogger('ocha-sync')


class OCHAImportException(Exception):
    pass


RETRY_ON_STATUS_CODES = {
    codes.bad_gateway,
    codes.gateway_timeout,
}

MAX_URL_RETRIES = 2
CACHE_URL_FOR = 300  # Seconds


def get_headers():
    username = settings.OCHA_API_USER
    password = settings.OCHA_API_PASSWORD

    headers = {}
    if username and password:
        auth_pair_str = '%s:%s' % (username, password)
        headers['Authorization'] = 'Basic ' + \
                                   base64.b64encode(auth_pair_str.encode()).decode()
    return headers


def get_json_from_url(url, retry_counter=MAX_URL_RETRIES):
    cached_response = cache.get(url)
    if cached_response:
        return cached_response

    def retry():
        sleep(5)
        return get_json_from_url(url, retry_counter=retry_counter - 1)

    logger.debug('Getting {}, attempt: {}'.format(url, MAX_URL_RETRIES - retry_counter + 1))
    try:
        response = requests.get(
            url,
            timeout=20,
            headers=get_headers()
        )
    except RequestException:
        return retry()

    if response.status_code in RETRY_ON_STATUS_CODES and retry_counter > 0:
        return retry()
    elif not response.status_code == codes.ok:
        raise OCHAImportException('Invalid response status code: {}'.format(response.status_code))

    response_json = response.json()
    if not response_json['status'] == 'ok':
        raise OCHAImportException('Invalid json response status: {}'.format(response_json['status']))
    cache.set(url, response_json, CACHE_URL_FOR)

    return response_json


def save_location_list(location_list, parent=None, save_children=False):
    location_ids = [l['id'] for l in location_list if 'id' in l and type(l['id']) == int]

    location_country_map = {}
    locations = []

    for location_id in sorted(location_ids):
        location = Location.objects.filter(
            external_source=EXTERNAL_DATA_SOURCES.HPC,
            external_id=location_id
        ).first()

        if not location or save_children:
            location_data = get_json_from_url(HPC_V2_ROOT_URL + 'location/{}'.format(location_id))
            if 'data' not in location_data:
                continue

        if not location:
            country = None
            if parent:
                country = parent.gateway.country
            elif location_data['data']['adminLevel'] == 0:
                country, _ = Country.objects.update_or_create(
                    country_short_code=location_data['data']['iso3'],
                    defaults={
                        'name': location_data['data']['name']
                    }
                )
                for child in location_data['data']['children']:
                    location_country_map[child['id']] = country
            elif location_data['data']['id'] in location_country_map:
                country = location_country_map[location_data['data']['id']]
                for child in location_data['data']['children']:
                    location_country_map[child['id']] = country
            elif not country:
                logger.warning('Couldn\'t find country for {}, skipping'.format(
                    HPC_V2_ROOT_URL + 'location/{}'.format(location_data['data']['id'])
                ))
                continue

            gateway_name = '{}-Admin Level {}'.format(country.country_short_code, location_data['data']['adminLevel'])
            logger.debug('Saving gateway type with name {}'.format(gateway_name))
            gateway, _ = GatewayType.objects.get_or_create(
                country=country,
                admin_level=location_data['data']['adminLevel'],
            )

            location, _ = Location.objects.update_or_create(
                gateway=gateway,
                title=location_data['data']['name'],
                defaults={
                    'external_source': EXTERNAL_DATA_SOURCES.HPC,
                    'external_id': location_data['data']['id'],
                    'latitude': location_data['data'].get('latitude'),
                    'longitude': location_data['data'].get('longitude'),
                    'parent': parent,
                }
            )
            logger.debug('Saved location {} as {}'.format(location_data['data']['id'], location))

        locations.append(location)

        if save_children:
            save_location_list(location_data['data'].get('children', []), parent=location)

    return locations


def save_disaggregations(disaggregation_categories, response_plan=None):
    category_to_group = get_disaggregation_category_to_group_map()

    disaggregations = []

    for category in disaggregation_categories:
        for category_id in category['ids']:
            if category_id in category_to_group:
                group_data = category_to_group[category_id]
                disaggregation, _ = Disaggregation.objects.update_or_create(
                    name=group_data['label'],
                    response_plan=response_plan
                )
                disaggregations.append(disaggregation)

                for category_data in group_data['disaggregationCategories']:
                    DisaggregationValue.objects.update_or_create(
                        value=category_data['label'],
                        disaggregation=disaggregation
                    )

    logger.debug('Saved {} disaggregations from {}'.format(
        len(disaggregations), disaggregation_categories
    ))

    return disaggregations


def save_cluster_objective(objective, child_activity=None):
    child_activity = child_activity or {}
    cluster_id = objective.get('parentId') or child_activity.get('parentId')
    cluster = Cluster.objects.filter(
        external_source=EXTERNAL_DATA_SOURCES.HPC,
        external_id=cluster_id,
    ).first()
    if not cluster:
        logger.error('Cluster #{} not found, skipping objective #{}'.format(
            cluster_id, objective['id']
        ))
        return None

    cluster_objective, _ = ClusterObjective.objects.update_or_create(
        external_id=objective['id'],
        external_source=EXTERNAL_DATA_SOURCES.HPC,
        defaults={
            'cluster': cluster,
            'title': objective['value']['description'][:2048]
        }
    )
    logger.debug('Saved Cluster Objective: {}'.format(cluster_objective))
    save_reportables_for_cluster_objective_or_activity(cluster_objective, objective['attachments'])
    return cluster_objective


def save_reportables_for_cluster_objective_or_activity(objective_or_activity, attachments):
    logger.debug('Saving {} reportables for {}'.format(len(attachments), objective_or_activity))
    reportables = []
    for attachment in attachments:
        if not attachment['type'] == 'indicator':
            continue

        values = attachment['value']['metrics']['values']['totals']
        disaggregated = attachment['value']['metrics']['values'].get('disaggregated', {})

        blueprint, _ = IndicatorBlueprint.objects.update_or_create(
            external_id=attachment['id'],
            external_source=EXTERNAL_DATA_SOURCES.HPC,
            defaults={
                'title': attachment['value']['description'],
                'disaggregatable': bool(disaggregated),
            }
        )

        target = get_dict_from_list_by_key(values, 'target').get('value', 0),
        baseline = get_dict_from_list_by_key(values, 'baseline').get('value', 0),
        in_need = get_dict_from_list_by_key(values, 'inNeed').get('value', 0),

        defaults = {
            'target': convert_to_json_ratio_value(target),
            'baseline': convert_to_json_ratio_value(baseline),
            'in_need': convert_to_json_ratio_value(in_need),
            'content_object': objective_or_activity,
            'blueprint': blueprint,
        }

        reportable, _ = Reportable.objects.update_or_create(
            external_id=attachment['id'],
            external_source=EXTERNAL_DATA_SOURCES.HPC,
            defaults={k: v for k, v in defaults.items() if v}
        )

        try:
            locations = save_location_list(
                attachment['value']['metrics']['values']['disaggregated']['locations']
            )
            logger.debug('Saving {} locations for {}'.format(
                len(locations), reportable
            ))

            for location in locations:
                ReportableLocationGoal.objects.get_or_create(
                    reportable=reportable,
                    location=location
                )

            objective_or_activity.locations.add(*locations)
            for disaggregation in save_disaggregations(
                disaggregated.get('categories', []), response_plan=objective_or_activity.cluster.response_plan
            ):
                reportable.disaggregations.through.objects.get_or_create(
                    reportable_id=reportable.id,
                    disaggregation_id=disaggregation.id
                )
        except (KeyError, TypeError, AttributeError):
            logger.warning('No location info found for {}'.format(reportable))

        reportables.append(reportable)

    objective_or_activity.reportables.add(*reportables)


def get_disaggregation_category_to_group_map():
    source_url = HPC_V2_ROOT_URL + 'disaggregation-category-group'
    group_category_list = get_json_from_url(source_url)['data']

    mapping = {}

    for group in group_category_list:
        for category in group['disaggregationCategories']:
            mapping[category['id']] = group

    return mapping

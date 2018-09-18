import logging
import datetime

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.db import transaction

from celery import shared_task

from rest_framework.exceptions import ValidationError

from core.api import PMP_API
from core.models import Workspace, GatewayType, Location, PRPRole
from core.serializers import PMPGatewayTypeSerializer, PMPLocationSerializer
from core.common import PARTNER_ACTIVITY_STATUS, PRP_ROLE_TYPES

from partner.models import PartnerActivity

from unicef.serializers import (
    PMPProgrammeDocumentSerializer,
    PMPPDPartnerSerializer,
    PMPPDPersonSerializer,
    PMPLLOSerializer,
    PMPPDResultLinkSerializer,
    PMPSectionSerializer,
    PMPReportingPeriodDatesSerializer,
    PMPReportingPeriodDatesSRSerializer,
)
from unicef.models import ProgrammeDocument, Person, LowerLevelOutput, PDResultLink, Section, ReportingPeriodDates

from indicator.serializers import PMPIndicatorBlueprintSerializer, PMPDisaggregationSerializer, \
    PMPDisaggregationValueSerializer, PMPReportableSerializer
from indicator.models import (
    IndicatorBlueprint,
    Disaggregation,
    Reportable,
    DisaggregationValue,
    ReportableLocationGoal,
    create_pa_reportables_from_ca,
)

from partner.models import Partner


logger = logging.getLogger(__name__)


User = get_user_model()
FIRST_NAME_MAX_LENGTH = User._meta.get_field('first_name').max_length
LAST_NAME_MAX_LENGTH = User._meta.get_field('last_name').max_length


def process_model(model_to_process, process_serializer, data, filter_dict):
    instance = model_to_process.objects.filter(**filter_dict).first()
    serializer = process_serializer(instance=instance, data=data)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def create_user_for_person(person):
    # Check if given person already exists in user model (by email)
    user, created = User.objects.get_or_create(username=person.email, defaults={
        'email': person.email
    })
    if created:
        user.set_unusable_password()

    if person.name:
        name_parts = person.name.split()
        if len(name_parts) == 2:
            user.first_name = name_parts[0][:FIRST_NAME_MAX_LENGTH]
            user.last_name = name_parts[1][:LAST_NAME_MAX_LENGTH]
        else:
            user.first_name = person.name[:FIRST_NAME_MAX_LENGTH]

    user.save()
    return user


def save_person_and_user(person_data):
    try:
        person = process_model(
            Person, PMPPDPersonSerializer, person_data, {'email': person_data['email']}
        )
    except ValidationError:
        logger.exception('Error trying to save Person model with {}'.format(person_data))
        return None, None

    user = create_user_for_person(person)

    return person, user


@shared_task
def process_programme_documents(fast=False, area=False):
    """
    Specifically each below expected_results instance has the following
    mapping.

    From this need to create indicator blueprint first, then disagg,
    then PDResultLink, then LL output, then Reportable attached to that LLO.
    {
        id: 8,                  --> LLO.external_id
        title: "blah",          --> LLO.title
        result_link: 47,        --> PDResultLink.external_id
        cp_output: {
            id: 312,            --> PDResultLink.external_cp_output_id
            title: "1.1 POLICY - NEWBORN & CHILD HEALTH"    --> PDResultLink.title
        },
        indicators: [ ]
    }
    """
    # # Get/Create Group that will be assigned to persons
    # partner_authorized_officer_group = PartnerAuthorizedOfficerRole.as_group()

    # Iterate over all workspaces
    if fast:
        workspaces = Workspace.objects.filter(business_area_code=area)  # 2130 for Iraq
    else:
        workspaces = Workspace.objects.all()

    with transaction.atomic():
        for workspace in workspaces:
            # Skip global workspace and Syria Cross Border / MENARO
            if workspace.business_area_code in ("0", "234R"):
                continue

            try:
                # Iterate over all pages
                page_url = None
                while True:
                    try:
                        api = PMP_API()
                        list_data = api.programme_documents(
                            business_area_code=str(
                                workspace.business_area_code), url=page_url)
                    except Exception as e:
                        print("API Endpoint error: %s" % e)
                        break

                    print(
                        "Found %s PDs for %s Workspace (%s)" %
                        (list_data['count'],
                         workspace.title,
                         workspace.business_area_code))

                    for item in list_data['results']:
                        print("Processing PD: %s" % item['id'])

                        # Get partner data
                        partner_data = item['partner_org']

                        # Skip entries without unicef_vendor_number
                        if not partner_data['unicef_vendor_number']:
                            print("No unicef_vendor_number - skipping!")
                            continue

                        # Create/Assign Partner
                        if not partner_data['name']:
                            print("No partner name - skipping!")
                            continue

                        partner_data['external_id'] = partner_data.get('id', '#')

                        try:
                            partner = process_model(
                                Partner,
                                PMPPDPartnerSerializer,
                                partner_data, {
                                    'vendor_number': partner_data['unicef_vendor_number']
                                }
                            )
                        except ValidationError:
                            logger.exception('Error trying to save Partner model with {}'.format(partner_data))

                        # Assign partner
                        item['partner'] = partner.id

                        # Assign workspace
                        item['workspace'] = workspace.id

                        # Modify offices entry
                        item['offices'] = ", ".join(
                            item['offices']) if item['offices'] else "N/A"

                        if not item['start_date']:
                            print("Start date is required - skipping!")
                            continue

                        if not item['end_date']:
                            print("End date is required - skipping!")
                            continue

                        # Create PD
                        item['status'] = item['status'].title()[:3]

                        # Amendment date formatting
                        for idx in range(len(item['amendments'])):
                            item['amendments'][idx]['signed_date'] = datetime.datetime.strptime(
                                item['amendments'][idx]['signed_date'], "%Y-%m-%d"
                            ).strftime("%d-%b-%Y")

                        try:
                            pd = process_model(
                                ProgrammeDocument, PMPProgrammeDocumentSerializer, item,
                                {'external_id': item['id'], 'workspace': workspace}
                            )
                        except KeyError as e:
                            if hasattr(e, 'message'):
                                print(e.message)
                            else:
                                print(e)

                            logger.exception('Error trying to save ProgrammeDocument model with {}'.format(item))
                            continue

                        # Create unicef_focal_points
                        person_data_list = item['unicef_focal_points']
                        for person_data in person_data_list:
                            person, user = save_person_and_user(person_data)
                            if not person:
                                continue

                            pd.unicef_focal_point.add(person)

                        # Create agreement_auth_officers
                        person_data_list = item['agreement_auth_officers']
                        for person_data in person_data_list:
                            person, user = save_person_and_user(person_data)
                            if not person:
                                continue

                            pd.unicef_officers.add(person)

                            user.partner = partner
                            user.save()

                            obj, created = PRPRole.objects.get_or_create(
                                user=user,
                                role=PRP_ROLE_TYPES.ip_authorized_officer,
                                workspace=workspace,
                            )

                            is_active = person_data.get('active')

                            if not created and obj.is_active and is_active is False:
                                obj.is_active = is_active
                                obj.save()

                        # Create focal_points
                        person_data_list = item['focal_points']
                        for person_data in person_data_list:
                            person, user = save_person_and_user(person_data)
                            if not person:
                                continue

                            pd.partner_focal_point.add(person)

                            user.partner = partner
                            user.save()

                            obj, created = PRPRole.objects.get_or_create(
                                user=user,
                                role=PRP_ROLE_TYPES.ip_authorized_officer,
                                workspace=workspace,
                            )

                            is_active = person_data.get('active')

                            if not created and obj.is_active and is_active is False:
                                obj.is_active = is_active
                                obj.save()

                        # Create sections
                        section_data_list = item['sections']
                        for section_data in section_data_list:
                            section = process_model(
                                Section, PMPSectionSerializer, section_data, {'external_id': section_data['id']}
                            )  # Is section unique globally or per workspace?
                            pd.sections.add(section)

                        # Create Reporting Date Periods for QPR and HR report type
                        reporting_requirements = item['reporting_requirements']
                        for reporting_requirement in reporting_requirements:
                            reporting_requirement['programme_document'] = pd.id
                            process_model(
                                ReportingPeriodDates,
                                PMPReportingPeriodDatesSerializer,
                                reporting_requirement,
                                {
                                    'external_id': reporting_requirement['id'],
                                    'report_type': reporting_requirement['report_type'],
                                    'programme_document': pd.id,
                                },
                            )

                        # Create Reporting Date Periods for SR report type
                        special_reports = item['special_reports'] if 'special_reports' in item else []
                        for special_report in special_reports:
                            special_report['programme_document'] = pd.id
                            special_report['report_type'] = 'SR'
                            process_model(
                                ReportingPeriodDates,
                                PMPReportingPeriodDatesSRSerializer,
                                special_report,
                                {
                                    'external_id': special_report['id'],
                                    'report_type': 'SR',
                                    'programme_document': pd.id,
                                },
                            )

                        if item['status'] not in ("draft, signed",):
                            # Mark all LLO/reportables assigned to this PD as inactive
                            llos = LowerLevelOutput.objects.filter(cp_output__programme_document=pd)
                            llos.update(active=False)
                            Reportable.objects.filter(lower_level_outputs__in=llos).update(active=False)

                            # Parsing expecting results and set them active, rest will stay inactive for this PD
                            for d in item['expected_results']:
                                # Create PDResultLink
                                rl = d['cp_output']
                                rl['programme_document'] = pd.id
                                rl['result_link'] = d['result_link']
                                pdresultlink = process_model(
                                    PDResultLink, PMPPDResultLinkSerializer,
                                    rl, {'external_id': rl['result_link'], 'external_cp_output_id': rl['id']}
                                )

                                # Create LLO
                                d['cp_output'] = pdresultlink.id
                                llo = process_model(
                                    LowerLevelOutput, PMPLLOSerializer, d, {'external_id': d['id']}
                                )
                                # Mark LLO as active
                                llo.active = True
                                llo.save()

                                # Iterate over indicators
                                for i in d['indicators']:
                                    # Check if indicator is cluster indicator
                                    i['is_cluster_indicator'] = True if i['cluster_indicator_id'] else False
                                    i['is_unicef_hf_indicator'] = i['is_high_frequency']

                                    # If indicator is not cluster, create Blueprint
                                    # otherwise use parent Blueprint
                                    if i['is_cluster_indicator']:
                                        # Get blueprint of parent indicator
                                        try:
                                            blueprint = Reportable.objects.get(
                                                id=i['cluster_indicator_id']).blueprint
                                        except Reportable.DoesNotExist:
                                            print("Blueprint not exists! Skipping!")
                                            continue
                                    else:
                                        # Create IndicatorBlueprint
                                        i['disaggregatable'] = True
                                        # TODO: Fix db schema to accommodate larger lengths
                                        i['title'] = i['title'][:255] if i['title'] else "unknown"

                                        if i['unit'] == '':
                                            if int(i['baseline']['d']) == 1:
                                                i['unit'] = 'number'
                                                i['display_type'] = 'number'

                                            elif int(i['baseline']['d']) != 1:
                                                i['unit'] = 'percentage'
                                                i['display_type'] = 'percentage'

                                        elif i['unit'] == 'number':
                                            i['display_type'] = 'number'

                                        blueprint = process_model(
                                            IndicatorBlueprint,
                                            PMPIndicatorBlueprintSerializer,
                                            i,
                                            {'external_id': i['blueprint_id']}
                                        )

                                    locations = list()
                                    for l in i['locations']:
                                        # Create gateway for location
                                        # TODO: assign country after PMP add these
                                        # fields into API
                                        country = workspace.countries.first()
                                        l['gateway_country'] = country.id

                                        if l['admin_level'] is None:
                                            print("Admin level empty! Skipping!")
                                            continue

                                        if l['pcode'] is None or not l['pcode']:
                                            print("Location code empty! Skipping!")
                                            continue

                                        l['location_type'] = '{}-Admin Level {}'.format(
                                            country.country_short_code,
                                            l['admin_level']
                                        )

                                        gateway = process_model(
                                            GatewayType,
                                            PMPGatewayTypeSerializer,
                                            l,
                                            {
                                                'admin_level': l['admin_level'],
                                                'country': l['gateway_country'],
                                            },
                                        )

                                        # Create location
                                        l['gateway'] = gateway.id
                                        location = process_model(
                                            Location,
                                            PMPLocationSerializer,
                                            l,
                                            {
                                                'gateway': l['gateway'],
                                                'p_code': l['pcode'],
                                            }
                                        )
                                        locations.append(location)

                                    # If indicator is not cluster, create
                                    # Disaggregation otherwise use parent
                                    # Disaggregation
                                    disaggregations = list()
                                    if i['is_cluster_indicator']:
                                        # Get Disaggregation
                                        try:
                                            disaggregations = list(
                                                Reportable.objects.get(
                                                    id=i['cluster_indicator_id']).disaggregations.all())
                                        except Reportable.DoesNotExist:
                                            disaggregations = list()
                                    else:
                                        # Create Disaggregation
                                        for dis in i['disaggregation']:
                                            dis['active'] = True
                                            disaggregation = process_model(
                                                Disaggregation, PMPDisaggregationSerializer,
                                                dis, {'name': dis['name']}
                                            )
                                            disaggregations.append(disaggregation)

                                            # Create Disaggregation Values
                                            for dv in dis['disaggregation_values']:
                                                dv['disaggregation'] = disaggregation.id
                                                process_model(
                                                    DisaggregationValue,
                                                    PMPDisaggregationValueSerializer,
                                                    dv,
                                                    {
                                                        'disaggregation_id': disaggregation.id,
                                                        'value': dv['value'],
                                                    }
                                                )

                                    # Create Reportable
                                    i['blueprint_id'] = blueprint.id if blueprint else None
                                    i['disaggregation_ids'] = [ds.id for ds in disaggregations]

                                    i['content_type'] = ContentType.objects.get_for_model(llo).id
                                    i['object_id'] = llo.id
                                    i['start_date'] = item['start_date']
                                    i['end_date'] = item['end_date']

                                    reportable = process_model(
                                        Reportable,
                                        PMPReportableSerializer,
                                        i,
                                        {'external_id': i['id']}
                                    )
                                    reportable.active = i['is_active']

                                    # TODO: Update the PMP PD indicator data field
                                    # for ca_indicator_used_by_reporting_entity

                                    partner_activity = None

                                    # Associate this LLO Reportable with ClusterActivity Reportable
                                    # for dual reporting
                                    if 'cluster_indicator_id' in i and i['cluster_indicator_id'] is not None:
                                        try:
                                            cai = Reportable.objects.get(id=int(i['cluster_indicator_id']))
                                            reportable.ca_indicator_used_by_reporting_entity = cai

                                            # Force adoption of PartnerActivity from ClusterActivity Indicator
                                            if pd.partner.id not in cai.partner_activities.values_list(
                                                    'partner', flat=True):
                                                try:
                                                    # TODO: Figure out what to put for
                                                    # project, start_date, end_date, and status
                                                    partner_activity = PartnerActivity.objects.create(
                                                        title=cai.title,
                                                        project=pd.partner.partner_projects.first(),
                                                        partner=pd.partner,
                                                        cluster_activity=cai,
                                                        start_date=cai.response_plan.start,
                                                        end_date=cai.response_plan.end,
                                                        status=PARTNER_ACTIVITY_STATUS.ongoing,
                                                    )
                                                except Exception as e:
                                                    print(
                                                        "Cannot associate PartnerActivity to ClusterActivity "
                                                        "for dual reporting - skipping link!"
                                                    )

                                                # Grab Cluster Activity instance from
                                                # this newly created Partner Activity instance
                                                create_pa_reportables_from_ca(partner_activity, cai)

                                        except Reportable.DoesNotExist:
                                            print(
                                                "No ClusterActivity Reportable found "
                                                "for dual reporting - skipping link!"
                                            )
                                        except Exception:
                                            print(
                                                "Invalid ClusterActivity Reportable ID "
                                                "for dual reporting - skipping link!"
                                            )

                                    reportable.save()

                                    rlgs = ReportableLocationGoal.objects.filter(reportable=reportable)

                                    # If the locations for this reportable has been created before
                                    if rlgs.exists():
                                        existing_locs = set(rlgs.values_list('location', flat=True))
                                        new_locs = set(map(lambda x: x.id, locations)) - existing_locs

                                        # Creating M2M Through model instances for new locations
                                        reportable_location_goals = [
                                            ReportableLocationGoal(
                                                reportable=reportable,
                                                location=l,
                                            ) for l in Location.objects.filter(id__in=new_locs)
                                        ]

                                    else:
                                        # Creating M2M Through model instances
                                        reportable_location_goals = [
                                            ReportableLocationGoal(
                                                reportable=reportable,
                                                location=l,
                                            ) for l in locations
                                        ]

                                    ReportableLocationGoal.objects.bulk_create(reportable_location_goals)

                                    if partner_activity:
                                        # Force update on PA Reportable instance for location update
                                        for pa_reportable in partner_activity.reportables.all():
                                            llo_locations = reportable.locations.values_list('id', flat=True)
                                            pai_locations = pa_reportable.locations.values_list('id', flat=True)
                                            loc_diff = pai_locations.exclude(id__in=llo_locations)

                                            # Add new locations from LLO Reportable to PA Reportable
                                            if loc_diff.exists():
                                                # Creating M2M Through model instances
                                                reportable_location_goals = [
                                                    ReportableLocationGoal(
                                                        reportable=reportable,
                                                        location=l,
                                                    ) for l in loc_diff
                                                ]

                                                ReportableLocationGoal.objects.bulk_create(reportable_location_goals)

                    # Check if another page exists
                    if list_data['next']:
                        print("Found new page")
                        page_url = list_data['next']
                    else:
                        print("End of workspace")
                        break
            except Exception as e:
                print(e)
                raise

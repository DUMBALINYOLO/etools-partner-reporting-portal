from __future__ import unicode_literals

import logging
from datetime import datetime, timedelta
from decimal import Decimal

import pycountry
from django.conf import settings
from django.contrib.gis.db import models
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator
)
from django.db.models import Q
from django.utils.encoding import python_2_unicode_compatible
from django.utils.functional import cached_property

from model_utils.models import TimeStampedModel
from mptt.models import MPTTModel, TreeForeignKey

from core.countries import COUNTRY_NAME_TO_ALPHA2_CODE
from .common import (
    RESPONSE_PLAN_TYPE,
    INDICATOR_REPORT_STATUS,
    OVERALL_STATUS,
    EXTERNAL_DATA_SOURCES,
    PRP_ROLE_TYPES,
)
from utils.emails import send_email_from_template
from utils.groups.wrappers import GroupWrapper


logger = logging.getLogger('locations.models')

# Define groups that UNICEF IP reporting users can belong to
try:
    PartnerAuthorizedOfficerRole = GroupWrapper(
        code='ip_authorized_officer', name='IP Authorized Officer', create_group=False
    )
    PartnerEditorRole = GroupWrapper(
        code='ip_editor', name='IP Editor', create_group=False
    )
    PartnerViewerRole = GroupWrapper(
        code='ip_viewer', name='IP Viewer', create_group=False
    )
    IMORole = GroupWrapper(code='imo', name='IMO', create_group=False)
except Exception as e:
    print("Group DB is not ready yet! - Error: %s" % e)


class TimeStampedExternalSyncModelMixin(TimeStampedModel):
    """
    A abstract class that provides external_id field that some models need since
    they might have been synced from an external system.
    """
    external_id = models.CharField(
        help_text='An ID representing this instance in an external system',
        blank=True,
        null=True,
        max_length=32
    )

    class Meta:
        abstract = True


class TimeStampedExternalSourceModel(TimeStampedExternalSyncModelMixin):
    external_source = models.TextField(choices=EXTERNAL_DATA_SOURCES, blank=True, null=True)

    class Meta:
        abstract = True
        unique_together = ('external_id', 'external_source')


class Country(TimeStampedModel):
    """
    Represents a country which has many offices and sections.
    Taken from https://github.com/unicef/etools/blob/master/EquiTrack/users/models.py
    on Sep. 14, 2017.
    """
    name = models.CharField(max_length=100)
    country_short_code = models.CharField(
        max_length=10,
        null=True,
        blank=True
    )
    long_name = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def details(self):
        """
        Tries to retrieve a usable country reference
        :return: pycountry Country object or None
        """
        lookup = None

        if not self.country_short_code:
            lookup = {'alpha_2': COUNTRY_NAME_TO_ALPHA2_CODE.get(self.name, None)}
        elif len(self.country_short_code) == 3:
            lookup = {'alpha_3': self.country_short_code}
        elif len(self.country_short_code) == 2:
            lookup = {'alpha_2': self.country_short_code}

        if lookup:
            try:
                return pycountry.countries.get(**lookup)
            except KeyError:
                pass


class Workspace(TimeStampedExternalSourceModel):
    """
    Workspace (previously called Workspace, also synonym was
    emergency/country) model.

    It's used for drop down menu in right top corner in the UI. Many times
    workspace is associated with only one country.
    """
    title = models.CharField(max_length=255)
    workspace_code = models.CharField(
        max_length=8,
        unique=True
    )
    countries = models.ManyToManyField(Country, related_name='workspaces')
    business_area_code = models.CharField(
        max_length=10,
        null=True, blank=True
    )
    latitude = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=5,
        validators=[
            MinValueValidator(Decimal(-90)),
            MaxValueValidator(Decimal(90))
        ]
    )
    longitude = models.DecimalField(
        null=True, blank=True,
        max_digits=8, decimal_places=5,
        validators=[
            MinValueValidator(Decimal(-180)),
            MaxValueValidator(Decimal(180))
        ]
    )
    initial_zoom = models.IntegerField(default=8)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def locations(self):
        """
        Returns a list of locations that belong to countries associated with
        this workspace.
        """
        result = self.countries.all().values_list(
            'gateway_types__locations').distinct()
        pks = []
        [pks.extend(filter(lambda x: x is not None, part)) for part in result]
        return Location.objects.filter(pk__in=pks)

    @property
    def can_import_ocha_response_plans(self):
        return any([
            c.details for c in self.countries.all()
        ])


class PRPRole(TimeStampedExternalSourceModel):
    """
    PRPRole model present a workspace-partner level permission entity
    with cluster association.

    related models:
        account.User (ForeignKey): "user"
    """
    user = models.ForeignKey(
        'account.User', related_name="prp_roles"
    )
    role = models.CharField(max_length=32, choices=PRP_ROLE_TYPES)
    workspace = models.ForeignKey(
        'core.Workspace', related_name="prp_roles",
        null=True, blank=True
    )
    cluster = models.ForeignKey(
        'cluster.Cluster', related_name="prp_roles",
        blank=True, null=True
    )

    def __str__(self):
        return '{} - {} in Workspace {}'.format(self.user, self.role, self.workspace)

    def send_email_notification(self, created):
        template_data = {
            'user': self.user,
            'role': self,
            'id_management_url': f'{settings.FRONTEND_HOST}/id-management/',
        }
        to_email_list = [self.user.email]
        content_subtype = 'html'

        if self.role == PRP_ROLE_TYPES.ip_admin:
            subject_template_path = 'emails/ip/notify_newly_designated_ip_admin_subject.txt'
            body_template_path = 'emails/ip/notify_newly_designated_ip_admin.html'
            template_data['training_materials_url'] = '#'  # TBD
        elif self.role in {PRP_ROLE_TYPES.ip_editor, PRP_ROLE_TYPES.ip_viewer}:
            if created:
                subject_template_path = 'emails/ip/notify_on_role_assignment_subject.txt'
                body_template_path = 'emails/ip/notify_on_role_assignment.html'
                template_data['training_materials_url'] = '#'  # TBD
            else:
                subject_template_path = 'emails/ip/notify_on_role_edit_subject.txt'
                body_template_path = 'emails/ip/notify_on_role_edit.html'
                template_data['training_materials_url'] = '#'   # TBD
        elif self.role == PRP_ROLE_TYPES.cluster_imo and created:
            subject_template_path = 'emails/cluster/notify_imo_on_role_assignment_subject.txt'
            body_template_path = 'emails/cluster/notify_imo_on_role_assignment.html'
            template_data['training_materials_url'] = '#'  # TBD
        elif self.role in {PRP_ROLE_TYPES.cluster_member,
                           PRP_ROLE_TYPES.cluster_viewer,
                           PRP_ROLE_TYPES.cluster_coordinator} and created:
            subject_template_path = 'emails/cluster/notify_on_role_assignment_subject.txt'
            body_template_path = 'emails/cluster/notify_on_role_assignment.html'
            template_data['training_materials_url'] = '#'  # TBD
            template_data['system_admin_email'] = '#'  # TBD
        else:
            return False

        send_email_from_template(
            subject_template_path=subject_template_path,
            body_template_path=body_template_path,
            template_data=template_data,
            to_email_list=to_email_list,
            content_subtype=content_subtype
        )
        return True


class ResponsePlan(TimeStampedExternalSourceModel):
    """
    ResponsePlan model present response of workspace (intervention).

    related models:
        ....
    """
    title = models.CharField(max_length=255, verbose_name='Response Plan')
    plan_type = models.CharField(
        max_length=3,
        choices=RESPONSE_PLAN_TYPE,
        default=RESPONSE_PLAN_TYPE.hrp,
        verbose_name='Plan Type'
    )
    start = models.DateField(
        null=True,
        blank=True,
        verbose_name='Start date'
    )
    end = models.DateField(
        null=True,
        blank=True,
        verbose_name='End date'
    )
    workspace = models.ForeignKey(
        'core.Workspace', related_name="response_plans"
    )

    class Meta:
        unique_together = ('title', 'plan_type', 'workspace')

    def __str__(self):
        return '#{} {}'.format(self.id, self.title)

    @property
    def documents(self):
        return []  # TODO probably create file field

    @cached_property
    def all_clusters(self):
        return self.clusters.all()

    @cached_property
    def can_import_ocha_projects(self):
        """
        We need external id and source to search projects for this plan
        """
        return bool(
            self.external_id and self.external_source == EXTERNAL_DATA_SOURCES.HPC
        )

    def num_of_partners(self, clusters=None):
        from partner.models import Partner

        if not clusters:
            clusters = self.all_clusters
        return Partner.objects.filter(clusters__in=clusters).distinct().count()

    def num_of_due_overdue_indicator_reports(self,
                                             clusters=None,
                                             partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_due_overdue_indicator_reports(partner=partner)
        return count

    def num_of_non_cluster_activities(self,
                                      clusters=None,
                                      partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_non_cluster_activities(partner=partner)
        return count

    def num_of_met_indicator_reports(self, clusters=None, partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_met_indicator_reports(partner=partner)
        return count

    def num_of_constrained_indicator_reports(
            self, clusters=None, partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_constrained_indicator_reports(partner=partner)
        return count

    def num_of_on_track_indicator_reports(self, clusters=None, partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_on_track_indicator_reports(partner=partner)
        return count

    def num_of_no_progress_indicator_reports(
            self, clusters=None, partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_no_progress_indicator_reports(partner=partner)
        return count

    def num_of_no_status_indicator_reports(self, clusters=None, partner=None):
        if not clusters:
            clusters = self.all_clusters

        count = 0
        for c in clusters:
            count += c.num_of_no_status_indicator_reports(partner=partner)
        return count

    def num_of_projects(self, clusters=None, partner=None):
        from partner.models import PartnerProject

        if not clusters:
            clusters = self.all_clusters

        qset = PartnerProject.objects.filter(clusters__in=clusters)
        if partner:
            qset = qset.filter(partner=partner)
        return qset.count()

    def _latest_indicator_reports(self, clusters):
        from indicator.models import Reportable, IndicatorReport
        reportables = Reportable.objects.filter(
            Q(partner_activities__partner__clusters__in=clusters)
        )
        return IndicatorReport.objects.filter(
            reportable__in=reportables).order_by(
            '-time_period_end').distinct()

    def upcoming_indicator_reports(self, clusters=None, partner=None,
                                   limit=None, days=15):
        if not clusters:
            clusters = self.all_clusters

        days_in_future = datetime.today() + timedelta(days=days)
        indicator_reports = self._latest_indicator_reports(clusters).filter(
            report_status=INDICATOR_REPORT_STATUS.due
        ).filter(
            due_date__gte=datetime.today()
        ).filter(
            due_date__lte=days_in_future
        )
        return indicator_reports

    def overdue_indicator_reports(self, clusters=None, partner=None,
                                  limit=None):
        """
        Returns indicator reports associated with partner activities or
        partner projects that are overdue, if partner is specified.
        """
        if not clusters:
            clusters = self.all_clusters

        indicator_reports = self._latest_indicator_reports(clusters)
        indicator_reports = indicator_reports.filter(
            report_status=INDICATOR_REPORT_STATUS.overdue)

        if partner:
            indicator_reports = indicator_reports.filter(
                Q(reportable__partner_projects__partner=partner)
                | Q(reportable__partner_activities__partner=partner)
            )

        if limit:
            indicator_reports = indicator_reports[:limit]

        return indicator_reports

    def constrained_indicator_reports(self, clusters=None, partner=None,
                                      limit=None):
        if not clusters:
            clusters = self.all_clusters

        indicator_reports = self._latest_indicator_reports(clusters)
        if partner:
            indicator_reports = indicator_reports.filter(
                Q(reportable__partner_projects__partner=partner)
                | Q(reportable__partner_activities__partner=partner)
            )
        indicator_reports = indicator_reports.filter(
            report_status=INDICATOR_REPORT_STATUS.accepted,
            overall_status=OVERALL_STATUS.constrained).order_by(
                'reportable__id', '-submission_date'
        ).distinct('reportable__id')
        if limit:
            indicator_reports = indicator_reports[:limit]
        return indicator_reports

    def partner_activities(self, partner, clusters=None, limit=None):
        if not clusters:
            clusters = self.all_clusters
        qset = partner.partner_activities.filter(
            partner__clusters__in=clusters)
        if limit:
            qset = qset[:limit]
        return qset


class GatewayType(TimeStampedModel):
    """
    Represents an Admin Type in location-related models.
    """

    name = models.CharField(max_length=64, unique=True)
    admin_level = models.PositiveSmallIntegerField()

    country = models.ForeignKey(Country, related_name="gateway_types")

    class Meta:
        ordering = ['name']
        verbose_name = 'Location Type'

    def __str__(self):
        return '{} - {}'.format(self.country, self.name)


class LocationManager(models.GeoManager):

    def get_queryset(self):
        return super(LocationManager, self).get_queryset(
        ).select_related('gateway')


@python_2_unicode_compatible
class Location(TimeStampedExternalSourceModel):
    """
    Location model define place where agents are working.
    The background of the location can be:
    Country > Region > City > District/Point.

    Either a point or geospatial object.
    pcode should be unique.

    related models:
        indicator.Reportable (ForeignKey): "reportable"
        core.Location (ForeignKey): "self"
        core.GatewayType: "gateway"
    """
    title = models.CharField(max_length=255)

    gateway = models.ForeignKey(
        GatewayType, verbose_name='Location Type', related_name='locations'
    )
    carto_db_table = models.ForeignKey(
        'core.CartoDBTable',
        related_name="locations",
        blank=True,
        null=True
    )

    latitude = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=5,
        validators=[
            MinValueValidator(Decimal(-90)),
            MaxValueValidator(Decimal(90))
        ]
    )
    longitude = models.DecimalField(
        null=True,
        blank=True,
        max_digits=8,
        decimal_places=5,
        validators=[
            MinValueValidator(Decimal(-180)),
            MaxValueValidator(Decimal(180))
        ]
    )
    p_code = models.CharField(max_length=32, blank=True, null=True, verbose_name='Postal Code')

    parent = models.ForeignKey(
        'self', null=True, blank=True, related_name='children', db_index=True
    )

    geom = models.MultiPolygonField(null=True, blank=True)
    point = models.PointField(null=True, blank=True)
    objects = LocationManager()

    class Meta:
        unique_together = ('title', 'p_code')
        ordering = ['title']

    def __str__(self):
        if self.p_code:
            return '{} ({} {})'.format(
                self.title,
                self.gateway.name,
                "{}: {}".format(
                    'CERD' if self.gateway.name == 'School' else 'PCode', self.p_code or ''
                ))

        return self.title

    @property
    def geo_point(self):
        return self.point if self.point else self.geom.point_on_surface if self.geom else ""

    @property
    def point_lat_long(self):
        return "Lat: {}, Long: {}".format(
            self.point.y,
            self.point.x
        )


class CartoDBTable(MPTTModel):
    """
    Represents a table in CartoDB, it is used to imports locations
    related models:
        core.GatewayType: 'gateway'
        core.Country: 'country'
    """

    domain = models.CharField(max_length=254)
    api_key = models.CharField(max_length=254)
    table_name = models.CharField(max_length=254)
    location_type = models.ForeignKey(GatewayType)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)

    country = models.ForeignKey(Country, related_name="carto_db_tables")

    def __str__(self):
        return self.table_name

from django.conf import settings

from account.models import User, UserProfile
from cluster.models import Cluster, ClusterObjective, ClusterActivity
from partner.models import (
    Partner,
    PartnerProject,
    PartnerActivity,
)
from indicator.models import (
    IndicatorBlueprint,
    Reportable,
    IndicatorReport,
)
from unicef.models import (
    ProgressReport,
    ProgrammeDocument,
    CountryProgrammeOutput,
    LowerLevelOutput,
)

from core.factories import (
    UserFactory,
    UserProfileFactory,
    ClusterFactory,
    ClusterObjectiveFactory,
    ClusterActivityFactory,
    PartnerFactory,
    PartnerProjectFactory,
    PartnerActivityFactory,
    IndicatorBlueprintFactory,
    ReportableToLowerLevelOutputFactory,
    IndicatorReportFactory,
    ProgressReportFactory,
    ProgrammeDocumentFactory,
    CountryProgrammeOutputFactory,
    LowerLevelOutputFactory,
)


def clean_up_data():
    if settings.ENV == 'dev':
        print "Deleting all ORM objects"

        User.objects.all().delete()
        Cluster.objects.all().delete()
        ClusterObjective.objects.all().delete()
        ClusterActivity.objects.all().delete()
        Partner.objects.all().delete()
        PartnerProject.objects.all().delete()
        PartnerActivity.objects.all().delete()
        IndicatorBlueprint.objects.all().delete()
        Reportable.objects.all().delete()
        IndicatorReport.objects.all().delete()
        ProgressReport.objects.all().delete()
        ProgrammeDocument.objects.all().delete()
        CountryProgrammeOutput.objects.all().delete()
        LowerLevelOutput.objects.all().delete()

        print "All ORM objects deleted"

def generate_fake_data(quantity=3):
    admin, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@unicef.org',
        'is_superuser': True,
        'is_staff': True
    })
    admin.set_password('Passw0rd!')
    admin.save()
    print "Superuser created:{}/{}".format(admin.username, 'Passw0rd!')

    UserFactory.create_batch(quantity)
    print "{} User objects created".format(quantity)

    ClusterFactory.create_batch(quantity)
    print "{} Cluster objects created".format(quantity)

    ClusterObjectiveFactory.create_batch(quantity)
    print "{} ClusterObjective objects created".format(quantity)

    ClusterActivityFactory.create_batch(quantity)
    print "{} ClusterActivity objects created".format(quantity)

    PartnerFactory.create_batch(quantity)
    print "{} Partner objects created".format(quantity)

    PartnerProjectFactory.create_batch(quantity)
    print "{} PartnerProject objects created".format(quantity)

    PartnerActivityFactory.create_batch(quantity)
    print "{} PartnerActivity objects created".format(quantity)

    IndicatorBlueprintFactory.create_batch(quantity)
    print "{} IndicatorBlueprint objects created".format(quantity)

    ReportableToLowerLevelOutputFactory.create_batch(quantity)
    print "{} ReportableToLowerLevelOutput objects created".format(quantity)

    IndicatorReportFactory.create_batch(quantity)
    print "{} IndicatorReport objects created".format(quantity)

    ProgressReportFactory.create_batch(quantity)
    print "{} ProgressReport objects created".format(quantity)

    ProgrammeDocumentFactory.create_batch(quantity)
    print "{} ProgrammeDocument objects created".format(quantity)

    CountryProgrammeOutputFactory.create_batch(quantity)
    print "{} CountryProgrammeOutput objects created".format(quantity)

    LowerLevelOutputFactory.create_batch(quantity)
    print "{} LowerLevelOutput objects created".format(quantity)

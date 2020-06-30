from django.conf.urls import url

from .views import (
    InterventionPMPDocumentView,
    PMPPartnerImportAPIView,
    ProgrammeDocumentAPIView,
    ProgrammeDocumentCalculationMethodsAPIView,
    ProgrammeDocumentDetailsAPIView,
    ProgrammeDocumentIndicatorsAPIView,
    ProgrammeDocumentLocationsAPIView,
    ProgrammeDocumentProgressAPIView,
    ProgressReportAnnexCPDFView,
    ProgressReportAPIView,
    ProgressReportAttachmentAPIView,
    ProgressReportAttachmentListCreateAPIView,
    ProgressReportDetailsAPIView,
    ProgressReportDetailsUpdateAPIView,
    ProgressReportExcelExportView,
    ProgressReportExcelImportView,
    ProgressReportIndicatorsAPIView,
    ProgressReportLocationsAPIView,
    ProgressReportPullHFDataAPIView,
    ProgressReportReviewAPIView,
    ProgressReportSRSubmitAPIView,
    ProgressReportSubmitAPIView,
)

urlpatterns = [
    url(r'^(?P<workspace_id>\d+)/programme-document/$',
        ProgrammeDocumentAPIView.as_view(),
        name="programme-document"),
    url(r'^(?P<workspace_id>\d+)/programme-document/(?P<pd_id>\d+)/$',
        ProgrammeDocumentDetailsAPIView.as_view(),
        name="programme-document-details"),
    url(r'^(?P<workspace_id>\d+)/programme-document/(?P<pd_id>\d+)/progress/$',
        ProgrammeDocumentProgressAPIView.as_view(),
        name="programme-document-progress"),
    url(r'^(?P<workspace_id>\d+)/programme-document/(?P<pd_id>\d+)/calculation-methods/$',
        ProgrammeDocumentCalculationMethodsAPIView.as_view(),
        name="programme-document-calculation-methods"),

    url(r'^(?P<workspace_id>\d+)/programme-document/locations/$',
        ProgrammeDocumentLocationsAPIView.as_view(),
        name="programme-document-locations"),
    url(r'^(?P<workspace_id>\d+)/programme-document/indicators/$',
        ProgrammeDocumentIndicatorsAPIView.as_view(),
        name="programme-document-indicators"),
    url(r'^(?P<workspace_id>\d+)/programme-document/(?P<pd_id>\d+)/pmp-document/$',
        InterventionPMPDocumentView.as_view(),
        name="programme-document-file"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/$',
        ProgressReportAPIView.as_view(),
        name="progress-reports"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/$',
        ProgressReportDetailsAPIView.as_view(),
        name="progress-reports-details"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/update/$',
        ProgressReportDetailsUpdateAPIView.as_view(),
        name="progress-reports-details"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/annex-C-export-PDF/$',
        ProgressReportAnnexCPDFView.as_view(),
        name="progress-reports-pdf"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/export/$',
        ProgressReportExcelExportView.as_view(),
        name="progress-reports-excel-export"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/import/$',
        ProgressReportExcelImportView.as_view(),
        name="progress-reports-excel-import"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/submit/$',
        ProgressReportSubmitAPIView.as_view(),
        name="progress-reports-submit"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/submit/sr/$',
        ProgressReportSRSubmitAPIView.as_view(),
        name="progress-reports-sr-submit"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/review/$',
        ProgressReportReviewAPIView.as_view(),
        name="progress-reports-review"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<pk>\d+)/indicators/(?P<indicator_report_pk>\d+)/pull/$',
        ProgressReportPullHFDataAPIView.as_view(),
        name="progress-reports-pull-hf-data"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<progress_report_id>\d+)/indicator-reports/$',
        ProgressReportIndicatorsAPIView.as_view(),
        name="progress-reports-indicators"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<progress_report_id>\d+)/locations/$',
        ProgressReportLocationsAPIView.as_view(),
        name="progress-reports-locations"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<progress_report_id>\d+)/attachments/$',
        ProgressReportAttachmentListCreateAPIView.as_view(),
        name="progress-reports-attachment-list"),
    url(r'^(?P<workspace_id>\d+)/progress-reports/(?P<progress_report_id>\d+)/attachments/(?P<pk>\d+)/$',
        ProgressReportAttachmentAPIView.as_view(),
        name="progress-reports-attachment"),

    url(r'^pmp/import/(?P<business_area_code>[^/]+)/partner/$',
        PMPPartnerImportAPIView.as_view(),
        name='pmp-import-partner'),
]

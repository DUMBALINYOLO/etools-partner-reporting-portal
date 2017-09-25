from django.contrib import admin

from .models import (
    IndicatorBlueprint,
    Reportable,
    IndicatorReport,
    IndicatorLocationData,
    Disaggregation,
    DisaggregationValue,
)


class IndicatorBlueprintAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'code', 'disaggregatable', 'display_type')
    list_filter = ('disaggregatable', 'unit',
                   'calculation_formula_across_periods',
                   'calculation_formula_across_locations',
                   'display_type')
    search_fields = ('title', 'description', 'code')


class ReportableAdmin(admin.ModelAdmin):
    list_display = ('blueprint', 'target', 'baseline', 'parent_indicator',
                    'frequency', 'assumptions', 'means_of_verification',
                    'is_cluster_indicator', 'start_date', 'end_date',
                    'cs_dates', 'content_object', 'content_type')
    list_filter = ('is_cluster_indicator',)
    search_fields = ('context_code', 'description', 'code', 'assumptions')


class IndicatorReportAdmin(admin.ModelAdmin):
    list_display = ('title', 'progress_report', 'time_period_start',
                    'time_period_end', 'due_date', 'submission_date',
                    'frequency', 'total', 'reportable')
    list_filter = ('frequency', 'report_status', 'overall_status')
    search_fields = ('title', 'narrative_assessment', 'remarks')


class IndicatorLocationDataAdmin(admin.ModelAdmin):
    list_display = ('indicator_report', 'location', 'num_disaggregation',
                    'level_reported')
    list_filter = ('num_disaggregation', 'level_reported',)


class DisaggregationAdmin(admin.ModelAdmin):
    list_display = ('name', 'response_plan', 'active')
    list_filter = ('response_plan', 'active')
    search_fields = ('name',)


class DisaggregationValueAdmin(admin.ModelAdmin):
    list_display = ('disaggregation', 'value')
    list_filter = ('disaggregation',)
    search_fields = ('value',)


admin.site.register(IndicatorBlueprint, IndicatorBlueprintAdmin)
admin.site.register(Reportable, ReportableAdmin)
admin.site.register(IndicatorReport, IndicatorReportAdmin)
admin.site.register(IndicatorLocationData, IndicatorLocationDataAdmin)
admin.site.register(Disaggregation, DisaggregationAdmin)
admin.site.register(DisaggregationValue, DisaggregationValueAdmin)

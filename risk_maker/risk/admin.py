from django.contrib import admin

from risk_maker.risk.models import RiskType, RiskField, Risk


class RiskFieldInline(admin.TabularInline):
    model = RiskField
    extra = 1
    fields = ('id', 'name', 'display_name', 'field_type', 'is_required', 'choices')


class RiskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    inlines = [RiskFieldInline,]
    search_field = ('name',)


class RiskFieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'risk_type', 'field_type', 'is_required')
    search_field = ('name', 'risk_type__name')


class RiskAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'risk_type')


admin.site.register(RiskType, RiskTypeAdmin)
admin.site.register(RiskField, RiskFieldAdmin)
admin.site.register(Risk, RiskAdmin)

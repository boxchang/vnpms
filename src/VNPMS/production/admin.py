from django.contrib import admin

from production.models import WorkType, Machine


@admin.register(WorkType)
class WorkTypeAdmin(admin.ModelAdmin):
    list_display = ('type_code', 'type_name', 'type_name_vi', 'type_name_en')


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('step_code', 'step_name', 'mach_code', 'mach_name')
from django.contrib import admin
from monitor.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = ('svr_no', 'svr_name', 'ip_addr', 'port', 'command', 'comment', 'update_at', 'update_by',)

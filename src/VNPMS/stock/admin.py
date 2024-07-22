from django.contrib import admin

from stock.models import Storage, Location, Bin, MovementType


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('storage_code', 'desc', 'enable')


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('storage', 'location_code', 'location_name', 'desc', 'enable')


@admin.register(Bin)
class BinAdmin(admin.ModelAdmin):
    list_display = ('location', 'bin_code', 'bin_name', 'enable')


@admin.register(MovementType)
class MovementTypeAdmin(admin.ModelAdmin):
    list_display = ('mvt_code', 'mvt_name', 'desc')
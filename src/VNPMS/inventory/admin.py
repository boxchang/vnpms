from django.contrib import admin
from inventory.models import ItemCategory, ItemType, Item, FormStatus, ItemFamily, Series


@admin.register(ItemFamily)
class ItemFamilyAdmin(admin.ModelAdmin):
    list_display = ('family_code', 'family_name', 'perm_group')


@admin.register(ItemCategory)
class ItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('catogory_code', 'category_name', 'manual')


@admin.register(ItemType)
class ItemTypeAdmin(admin.ModelAdmin):
    list_display = ('category', 'type_code', 'type_name', 'is_attached')


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'sap_code', 'vendor_code', 'item_type', 'spec', 'price', 'unit', 'enabled')


@admin.register(FormStatus)
class FormStatusAdmin(admin.ModelAdmin):
    list_display = ('status_name',)


@admin.register(Series)
class FormStatusAdmin(admin.ModelAdmin):
    list_display = ('key', 'series', 'desc')
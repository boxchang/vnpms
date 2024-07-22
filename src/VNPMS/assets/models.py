from django.contrib.auth.models import Group
from django.urls import reverse
from django.db import models
from django.conf import settings


class Label_attachment(models.Model):
    files = models.FileField(upload_to='uploads/label/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='label_create_by')  # 建立者

class Pic_attachment(models.Model):
    asset = models.ForeignKey(
        'Asset', related_name='asset_pics', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/picture/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='pic_create_by')  # 建立者

class Doc_attachment(models.Model):
    asset = models.ForeignKey(
        'Asset', related_name='asset_docs', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/document/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='doc_create_by')  # 建立者


class AssetArea(models.Model):
    area_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='area_create_by')  # 建立者

    def __str__(self):
        return self.area_name


class AssetCategory(models.Model):
    category_name = models.CharField(max_length=50, blank=False, null=False)
    perm_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name='category_group', null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='category_create_by')  # 建立者

    def __str__(self):
        return self.category_name

class AssetType(models.Model):
    category = models.ForeignKey(
        AssetCategory, related_name='category_type', on_delete=models.CASCADE)
    type_name = models.CharField(max_length=50, blank=False, null=False)
    type_code = models.CharField(max_length=50, blank=False, null=False)
    prefix = models.CharField(max_length=50, blank=True, null=True)
    series_len = models.IntegerField(default=5)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='type_create_by')  # 建立者

    def __str__(self):
        return self.type_name

    class Meta:
        ordering = ['type_name']

class Unit(models.Model):
    unit_no = models.CharField(max_length=50, blank=False, null=False)
    unit_name = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.unit_name


class Brand(models.Model):
    category = models.ForeignKey(
        AssetCategory, related_name='category_brand', on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='brand_create_by')  # 建立者

    def __str__(self):
        return self.brand_name

    class Meta:
        ordering = ['brand_name']

class Location(models.Model):
    location_name = models.CharField(max_length=50, blank=False, null=False)
    location_code = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='location_create_by')  # 建立者

    def __str__(self):
        return self.location_name

    class Meta:
        ordering = ['location_name']

class AssetStatus(models.Model):
    status_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='status_create_by')  # 建立者

    def __str__(self):
        return self.status_name


class Asset(models.Model):
    asset_no = models.CharField(max_length=50, blank=False, null=False, unique=True)
    label_no = models.CharField(max_length=50, blank=True, null=True, unique=True)
    auto_encode = models.BooleanField(default=True)
    category = models.ForeignKey(
        AssetCategory, related_name='asset_category', on_delete=models.DO_NOTHING)
    type = models.ForeignKey(
        AssetType, related_name='asset_type', on_delete=models.DO_NOTHING)
    brand = models.ForeignKey(
        Brand, related_name='asset_brand', on_delete=models.DO_NOTHING)
    model = models.CharField(max_length=50, blank=True, null=True)
    desc = models.CharField(max_length=1000, blank=True, null=True)
    area = models.ForeignKey(
        AssetArea, related_name='asset_area', on_delete=models.DO_NOTHING)
    owner_unit = models.ForeignKey(Unit, related_name='asset_owner_unit', on_delete=models.DO_NOTHING, blank=False, null=False)
    keeper_unit = models.ForeignKey(Unit, related_name='asset_keeper_unit', on_delete=models.DO_NOTHING, blank=True, null=True)
    keeper_no = models.CharField(max_length=50, blank=True, null=True)
    keeper_name = models.CharField(max_length=50, blank=True, null=True)
    location = models.ForeignKey(
        Location, related_name='asset_location', on_delete=models.DO_NOTHING)
    location_desc = models.CharField(max_length=50, blank=True, null=True)
    pur_date = models.CharField(max_length=50, blank=True, null=True)
    pur_price = models.CharField(max_length=50, blank=False, null=False)
    status = models.ForeignKey(
        AssetStatus, related_name='asset_status', on_delete=models.DO_NOTHING)
    enabled = models.BooleanField(default=True)
    sap_asset_no = models.CharField(max_length=50, blank=True, null=True)
    scrap_date = models.CharField(max_length=50, blank=True, null=True)
    scrap_reason = models.CharField(max_length=1000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='asset_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='asset_update_by')
    comment = models.CharField(max_length=5000, blank=True, null=True)

    def __str__(self):
        return self.label_no

    def get_absolute_url(self):
        return reverse('assets_detail', kwargs={'pk': self.pk})


class Series(models.Model):
    key = models.CharField(max_length=50, blank=False, null=False)
    series = models.IntegerField()
    desc = models.CharField(max_length=50, blank=True, null=True)


class History(models.Model):
    asset = models.ForeignKey(Asset, related_name='asset_history', on_delete=models.CASCADE)
    attr_code = models.CharField(max_length=20, blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True, null=True)
    before = models.CharField(max_length=20, blank=True, null=True)
    after = models.CharField(max_length=20, blank=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='hist_update_by')
    update_at = models.DateTimeField(auto_now=True, null=True)

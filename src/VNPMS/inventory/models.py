from django.contrib.auth.models import Group
from django.db import models
from django.conf import settings
from datetime import datetime
from django.urls import reverse
from users.models import Unit


class FormStatus(models.Model):
    status_name = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='form_status_create_by')  # 建立者

    def __str__(self):
        return self.status_name


class ItemFamily(models.Model):
    family_code = models.CharField(max_length=2, blank=False, null=False)
    family_name = models.CharField(max_length=50, blank=False, null=False)
    perm_group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, related_name='family_group', null=True,
                                   blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='item_family_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='item_family_update_by')

    def __str__(self):
        return self.family_name


class ItemCategory(models.Model):
    family = models.ForeignKey(ItemFamily, related_name='category_family', on_delete=models.CASCADE)
    catogory_code = models.CharField(max_length=2, blank=False, null=False)
    category_name = models.CharField(max_length=50, blank=False, null=False)
    manual = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='item_category_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_category_update_by')

    def __str__(self):
        return self.category_name


class ItemType(models.Model):
    category = models.ForeignKey(
        ItemCategory, related_name='type_category', on_delete=models.CASCADE)
    type_code = models.CharField(max_length=2, blank=False, null=False)
    type_name = models.CharField(max_length=50, blank=False, null=False)
    is_attached = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='item_type_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_type_update_by')

    def __str__(self):
        return self.type_name


class Item(models.Model):
    item_code = models.CharField(max_length=11, blank=False, null=False)
    sap_code = models.CharField(max_length=20, blank=True, null=True)
    vendor_code = models.CharField(max_length=20, blank=True, null=True)
    unit = models.CharField(max_length=10, blank=False, null=False)
    item_type = models.ForeignKey(ItemType, related_name='item_type', on_delete=models.CASCADE)
    spec = models.CharField(max_length=2000, blank=True, null=True)
    price = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    is_stock = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_update_by')

    def __str__(self):
        return self.spec

    def get_absolute_url(self):
        return reverse('item_detail', kwargs={'pk': self.pk})

class Pic_attachment(models.Model):
    item = models.ForeignKey('Item', related_name='item_pics', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/picture/item/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='item_pic_create_by')  # 建立者


class AppliedForm(models.Model):
    form_no = models.CharField(max_length=20, primary_key=True)
    unit = models.ForeignKey(Unit, related_name='applied_unit', on_delete=models.DO_NOTHING)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='applied_form_requester')
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='applied_form_approver', blank=True, null=True)
    approve_time = models.DateTimeField(null=True)
    apply_date = models.CharField(max_length=10, blank=False, null=False)
    category = models.ForeignKey(ItemCategory, related_name='form_category', on_delete=models.DO_NOTHING)
    status = models.ForeignKey(FormStatus, related_name='form_status', on_delete=models.DO_NOTHING)
    ext_number = models.CharField(max_length=20, blank=True, null=True)
    reason = models.CharField(max_length=2000, blank=True, null=True)
    admin_comment = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='inv_form_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='inv_form_update_by')

    def get_absolute_url(self):
        return reverse('inv_detail', kwargs={'pk': self.pk})


class AppliedItem(models.Model):
    applied_form = models.ForeignKey(AppliedForm, related_name='applied_form_item', on_delete=models.CASCADE)
    category = models.CharField(max_length=50)
    item_code = models.CharField(max_length=11)
    spec = models.CharField(max_length=200)
    model = models.CharField(max_length=200, blank=True, null=True)
    qty = models.IntegerField(default=0)
    unit = models.CharField(max_length=10)
    comment = models.CharField(max_length=2000, blank=True, null=True)
    received_qty = models.IntegerField(default=0)


class Apply_attachment(models.Model):
    apply = models.ForeignKey('AppliedForm', related_name='apply_files', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/inventory/apply/%Y/%m/')
    description = models.CharField(max_length=50, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='form_files_create_by')  # 建立者


class Series(models.Model):
    key = models.CharField(max_length=50, blank=False, null=False)
    series = models.IntegerField()
    desc = models.CharField(max_length=50, blank=True, null=True)


class Setting(models.Model):
    attr = models.CharField(max_length=50, blank=False, null=False)
    values = models.CharField(max_length=500, blank=False, null=False)


class Template_attachment(models.Model):
    key_file = models.FileField(upload_to='inventory/template/')
    stamp_file = models.FileField(upload_to='inventory/template/')
    print_file = models.FileField(upload_to='inventory/template/')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='template_update_by')


from django.db import models
from django.conf import settings
from django.urls import reverse

from inventory.models import Item


class MovementType(models.Model):
    mvt_code = models.CharField(max_length=5, primary_key=True)
    mvt_name = models.CharField(max_length=20, blank=False, null=False)
    desc = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='mvt_create_by')  # 建立者

    def __str__(self):
        return self.desc


class Storage(models.Model):
    storage_code = models.CharField(max_length=6, primary_key=True)
    desc = models.CharField(max_length=200, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='storage_update_by')
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.desc


class Location(models.Model):
    storage = models.ForeignKey(Storage, related_name='storage_location', on_delete=models.DO_NOTHING)
    location_code = models.CharField(max_length=10, primary_key=True)
    location_name = models.CharField(max_length=20, blank=False, null=False)
    desc = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='location_update_by')

    def __str__(self):
        return self.desc


class Bin(models.Model):
    location = models.ForeignKey(Location, related_name='location_bin', on_delete=models.DO_NOTHING)
    bin_code = models.CharField(max_length=20, primary_key=True)
    bin_name = models.CharField(max_length=200, blank=True, null=True)
    enable = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='bin_update_by')

    def __str__(self):
        return self.bin_name


class Stock(models.Model):
    item = models.ForeignKey(Item, related_name='stock_item', on_delete=models.DO_NOTHING)
    bin = models.ForeignKey(Bin, related_name='stock_bin', on_delete=models.DO_NOTHING)
    qty = models.IntegerField(default=0)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='stock_update_by')


class StockHistory(models.Model):
    batch_no = models.CharField(max_length=20, blank=False, null=False)
    mtr_doc = models.CharField(max_length=10, blank=True, null=True)
    item = models.ForeignKey(Item, related_name='stock_hist_item', on_delete=models.DO_NOTHING)
    bin = models.ForeignKey(Bin, related_name='stock_hist_bin', on_delete=models.DO_NOTHING)
    mvt = models.ForeignKey(MovementType, related_name='stock_hist_mvt', on_delete=models.DO_NOTHING)
    plus_qty = models.IntegerField(default=0)
    minus_qty = models.IntegerField(default=0)
    remain_qty = models.IntegerField(default=0)
    desc = models.CharField(max_length=200, blank=True, null=True)
    create_at = models.DateTimeField(auto_now=True, null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='stock_hist_update_by')


class StockInForm(models.Model):
    form_no = models.CharField(max_length=20, primary_key=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='stockin_form_requester')
    apply_date = models.CharField(max_length=10, blank=False, null=False)
    pr_no = models.CharField(max_length=100, blank=True, null=True)
    reason = models.CharField(max_length=2000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='stockin_form_create_by')  # 建立者

    def get_absolute_url(self):
        return reverse('stockin_detail', kwargs={'pk': self.pk})


class StockOutForm(models.Model):
    form_no = models.CharField(max_length=20, primary_key=True)
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='stockout_form_requester')
    apply_date = models.CharField(max_length=10, blank=False, null=False)
    reason = models.CharField(max_length=2000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='stockout_form_create_by')  # 建立者

    def get_absolute_url(self):
        return reverse('stockout_detail', kwargs={'pk': self.pk})



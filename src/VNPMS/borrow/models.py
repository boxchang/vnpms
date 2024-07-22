from django.db import models
from django.conf import settings
from assets.models import Asset
from datetime import datetime

class Borrow(models.Model):
    form_no = models.AutoField(primary_key=True)
    app_dept = models.CharField(max_length=50, blank=False, null=False)
    app_user = models.CharField(max_length=50, blank=False, null=False)
    comment = models.CharField(max_length=500, blank=False, null=False)
    apply_date = models.CharField(max_length=10, blank=False, null=False)
    expect_date = models.CharField(max_length=10, blank=False, null=False)
    lend_date = models.CharField(max_length=10, blank=True, null=True)
    lend_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='lend_owner', null=True)
    return_date = models.CharField(max_length=10, blank=True, null=True)
    return_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='return_owner', null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='borrow_update_by', null=True)
    admin_comment = models.CharField(max_length=500, blank=False, null=False)
    finished = models.BooleanField(default=False)


class BorrowItem(models.Model):
    borrow = models.ForeignKey(Borrow, related_name='borrow_item', on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, related_name='borrow_asset', on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.asset.label_no + " " + self.asset.model + " " + self.asset.desc


class BPMDept(models.Model):
    class Meta:
        managed = False

    dept_no = models.CharField(max_length=50, blank=False, null=False, unique=True)
    dept_name = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.dept_name


class BPMUser(models.Model):
    class Meta:
        managed = False

    user_no = models.CharField(max_length=50, blank=False, null=False, unique=True)
    user_name = models.CharField(max_length=50, blank=False, null=False, unique=True)

    def __str__(self):
        return self.user_name



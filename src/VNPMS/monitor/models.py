from django.db import models
from django.conf import settings
from users.models import Unit


class Config(models.Model):
    svr_no = models.CharField(max_length=2, unique=True)  # 序號
    svr_name = models.CharField(max_length=50, blank=False, null=False)
    ip_addr = models.CharField(max_length=15, blank=False, null=False)
    port = models.CharField(max_length=50, blank=False, null=False)
    command = models.CharField(max_length=50, blank=True, null=True)
    comment = models.CharField(max_length=2000, blank=True, null=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='svr_config_create_by')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='svr_config_update_by')

from django.db import models
from django.utils import timezone
from django.conf import settings


class Status(models.Model):
    status_en = models.CharField(max_length=50)
    status_cn = models.CharField(max_length=50)
    status_desc = models.TextField()
    process_rate = models.IntegerField(default=0)
    create_at = models.DateTimeField(default=timezone.now)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='status_create_at')
    update_at = models.DateTimeField(default=timezone.now)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='status_update_at')

    def __str__(self):
        return self.status_en


class DataIndex(models.Model):
    project = models.ForeignKey(
        'projects.Project', related_name='index_project', on_delete=models.CASCADE)
    data_type = models.CharField(max_length=10)
    data_date = models.CharField(max_length=8)
    current = models.IntegerField(default=0, null=True, blank=True)
    update_at = models.DateTimeField(default=timezone.now)


class FormType(models.Model):
    tid = models.IntegerField()
    type = models.CharField(max_length=8)
    short_name = models.CharField(max_length=3, null=False)


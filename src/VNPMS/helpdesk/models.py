from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.urls import reverse


class Helpdesk(models.Model):
    help_no = models.CharField(max_length=10, unique=True)  # 單號
    help_type = models.ForeignKey(
        'helpdesk.HelpdeskType', related_name='helpdesk_help_type', on_delete=models.DO_NOTHING)  # 類型
    title = models.CharField(max_length=100)
    desc = RichTextUploadingField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='helpdesk_create_at')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)  # 修改日期
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='helpdesk_update_at')  # 修改者

    def get_absolute_url(self):
        return reverse('helpdesk_search')


class Helpdesk_attachment(models.Model):
    helpdesk = models.ForeignKey(
        'Helpdesk', related_name='helpdesk_files', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/helpdesk/%Y/%m/')
    description = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=True)


class HelpdeskType(models.Model):
    tid = models.IntegerField()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.type

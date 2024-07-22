import os

from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.dispatch import receiver

# desc = RichTextUploadingField(null=True, blank=True, external_plugin_resources=[(
#         'youtube',
#         '/static/ckeditor/ckeditor/plugins/youtube',
#         'plugin.js', )],)


class Request(models.Model):
    request_no = models.CharField(
        'Request No.', max_length=20, unique=True)  # 需求單號
    title = models.CharField(max_length=100)  # 標題
    desc = RichTextUploadingField(null=True, blank=True, external_plugin_resources=[(
        'youtube',
        '/static/ckeditor/ckeditor/plugins/youtube',
        'plugin.js', )],)
    level = models.ForeignKey(
        'requests.Level', related_name='request_level', on_delete=models.DO_NOTHING)  # 緊急程度
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='request_owner',
                              on_delete=models.DO_NOTHING, null=True, blank=True)  # 需求負責人
    start_date = models.DateField(null=True, blank=True)  # 需求開始日期
    due_date = models.DateField(null=True, blank=True)  # 完工日期
    actual_date = models.DateField(null=True, blank=True)  # 實際完成日期
    status = models.ForeignKey(
        'bases.Status', related_name='request_level', on_delete=models.DO_NOTHING)  # 狀態
    is_test = models.BooleanField(default=False)  # 是否需要進行測試
    test_data = models.BooleanField(default=False)  # 是否有測試資料
    process_rate = models.IntegerField(
        default=0, null=True, blank=True)  # 完成度 系統運算
    belong_to = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True)  # 上層
    file_list = models.CharField(max_length=200, blank=True)  # 要卡控檔案上限
    project = models.ForeignKey(
        'projects.Project', related_name='request_project', on_delete=models.CASCADE)  # 歸屬專案
    estimate_time = models.IntegerField(
        default=0, null=True, blank=True)  # 預估時間(hr)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='request_create_at')  # 建立者
    update_at = models.DateTimeField(auto_now=True, null=True)  # 修改日期
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='request_update_at')  # 修改者

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})


class Level(models.Model):
    level_en = models.CharField(max_length=50)
    level_cn = models.CharField(max_length=50)
    level_desc = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='level_create_at')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='level_update_at')

    def __str__(self):
        return self.level_cn


class Request_attachment(models.Model):
    request = models.ForeignKey(
        'Request', related_name='request_files', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/requests/%Y/%m/')
    description = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=True)


@receiver(models.signals.post_delete, sender=Request_attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.files:
        if os.path.isfile(instance.files.path):
            os.remove(instance.files.path)

class Request_reply(models.Model):
    request = models.ForeignKey(
        'Request', related_name='request_reply', on_delete=models.CASCADE)
    desc = RichTextUploadingField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='request_reply_create_at')  # 建立者

    def get_absolute_url(self):
        return reverse('request_detail', kwargs={'pk': self.pk})
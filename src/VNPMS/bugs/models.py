import os

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django.conf import settings


class Bug(models.Model):
    bug_no = models.CharField('Bug No.', max_length=20, unique=True)
    belong_to = models.ForeignKey(
        'requests.Request', related_name='bug_super', on_delete=models.CASCADE, null=True)  # 上層
    title = models.CharField(max_length=100)
    status = models.ForeignKey(
        'bases.Status', related_name='bug_status', on_delete=models.DO_NOTHING)
    level = models.ForeignKey(
        'requests.Level', related_name='bus_level', on_delete=models.DO_NOTHING)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='bugs', on_delete=models.DO_NOTHING, null=True)
    project = models.ForeignKey(
        'projects.Project', related_name='bug_project', on_delete=models.CASCADE)
    desc = RichTextUploadingField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='bug_create_at')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='bug_update_at')

    def get_absolute_url(self):
        return reverse('bug_detail', kwargs={'pk': self.pk})


class Bug_attachment(models.Model):
    bug = models.ForeignKey(
        'Bug', related_name='bug_files', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/bugs/%Y/%m/')
    description = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, editable=True)


@receiver(models.signals.post_delete, sender=Bug_attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.files:
        if os.path.isfile(instance.files.path):
            os.remove(instance.files.path)

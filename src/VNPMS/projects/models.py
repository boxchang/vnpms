from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.urls import reverse


class Project(models.Model):
    name = models.CharField(max_length=100)
    short_name = models.CharField(max_length=3)
    desc = RichTextUploadingField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_create_dt',
                                  on_delete=models.DO_NOTHING)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='project_update_dt',
                                  on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('project_manage', kwargs={'pk': self.pk})


class Project_setting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='setting_user',
                             on_delete=models.CASCADE)
    project = models.ManyToManyField(
        'projects.Project', related_name='setting_project')
    default = models.ForeignKey('projects.Project', related_name='setting_default',
                                null=True, blank=True, on_delete=models.CASCADE)
    page_number = models.IntegerField(default=10)
    update_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user",),)

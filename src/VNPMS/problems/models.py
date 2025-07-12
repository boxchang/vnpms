import os

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

from users.models import Unit, Plant


class ProblemTypeList(models.Model):
    list_name = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=500, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='problem_type_list_create_at')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='problem_type_list_update_at')

    def __str__(self):
        return self.list_name


class ProblemType(models.Model):
    type_name = models.CharField(max_length=50, blank=True)
    belong_to = models.ForeignKey(ProblemTypeList, null=True, blank=True, related_name='type_list', on_delete=models.DO_NOTHING)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='problemtype_create_by')

    def __str__(self):
        return self.type_name

class Problem(models.Model):
    problem_no = models.CharField('Problem No.', max_length=20, unique=True)
    problem_datetime = models.CharField('Problem Datetime', max_length=20, blank=True, null=True)
    expected_datetime = models.CharField('Problem Datetime', max_length=20, blank=True, null=True)
    finish_datetime = models.CharField('Problem Datetime', max_length=20, blank=True, null=True)
    plant = models.ForeignKey(Plant, null=True, blank=True, related_name='problem_plant', on_delete=models.DO_NOTHING)
    dept = models.ForeignKey(Unit, null=True, blank=True, related_name='problem_dept', on_delete=models.DO_NOTHING)
    requester = models.CharField('Owner', max_length=80, blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='problem_owner',
                              on_delete=models.DO_NOTHING, null=True, blank=True)
    problem_type = models.ForeignKey(
        'problems.ProblemType',
        related_name='problem_type',
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    problem_status = models.ForeignKey(
        'bases.Status', related_name='problem_status', on_delete=models.DO_NOTHING)  # 狀態
    title = models.CharField(max_length=100)
    project = models.ForeignKey(
        'projects.Project', related_name='problem_super', on_delete=models.CASCADE)
    desc = RichTextUploadingField(null=True, blank=True)
    root_cause = RichTextUploadingField(null=True, blank=True)
    short_term = RichTextUploadingField(null=True, blank=True)
    long_term = RichTextUploadingField(null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='problem_create_at')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='problem_update_at')

    def __str__(self):
        return self.problem_no

    def __repr__(self):
        return self.problem_no

    def get_reply_count(self):
        return self.replys.count()

    def get_absolute_url(self):
        return reverse('problem_detail', kwargs={'pk': self.pk})

    @property
    def type_name(self):
        return "Problem"


class Problem_reply(models.Model):
    problem_no = models.ForeignKey(
        Problem, related_name='replys', on_delete=models.CASCADE)
    comment = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='reply_create_by')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='reply_update_by')


class Problem_attachment(models.Model):
    problem = models.ForeignKey(
        'Problem', related_name='problem_files', on_delete=models.CASCADE)
    files = models.FileField(upload_to='uploads/problems/%Y/%m/')
    description = models.CharField(max_length=50, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)


@receiver(models.signals.post_delete, sender=Problem_attachment)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.files:
        if os.path.isfile(instance.files.path):
            os.remove(instance.files.path)
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.db import models
from django.urls import reverse


class Request_test(models.Model):
    request = models.ForeignKey(
        'requests.Request', related_name='request_test', on_delete=models.CASCADE)
    desc = RichTextUploadingField(null=True, blank=True)
    version = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='rtest_create_by')
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='rtest_update_by')

    def __str__(self):
        return self.request.title+' Test'

    def __repr__(self):
        return self.request.title+' Test'

    def get_owner(self):  # Admin介面把多筆用逗號串起來
        return ",".join([str(p) for p in self.owner.all()])

    def get_absolute_url(self):
        return reverse('rtest_form', kwargs={'pk': self.pk})


class Request_test_item(models.Model):
    test = models.ForeignKey(
        'tests.Request_test', related_name='item_test', on_delete=models.CASCADE)
    item = models.CharField(max_length=100, blank=True)


class Test_result(models.Model):
    request = models.ForeignKey(
        'requests.Request', related_name='test_result_request', on_delete=models.CASCADE)
    tester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                               related_name='tester_result')
    result = models.BooleanField()
    create_at = models.DateTimeField(auto_now_add=True, editable=True)


class Test_result_detail(models.Model):
    test_result = models.ForeignKey(
        'tests.Test_result', related_name='result_detail', on_delete=models.CASCADE)
    item = models.ForeignKey('tests.Request_test_item',
                             related_name='result_item', on_delete=models.DO_NOTHING)
    item_result = models.BooleanField()

    def __str__(self):
        return self.item + '__' + str(self.result)

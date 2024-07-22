from django.db import models
from django.conf import settings
from django.urls import reverse


class ExcelTemp(models.Model):
    batch_no = models.CharField(max_length=20, primary_key=True)
    plant = models.CharField(max_length=10, blank=True, null=True)
    wo_no = models.CharField(max_length=20, blank=True, null=True)
    cfm_code = models.CharField(max_length=20, blank=True, null=True)
    ctr_code = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    work_center = models.CharField(max_length=20, blank=False, null=False)
    item_no = models.CharField(max_length=20, blank=True, null=True)
    spec = models.CharField(max_length=100, blank=True, null=True)
    step_no = models.CharField(max_length=20, blank=True, null=True)
    step_code = models.CharField(max_length=20, blank=True, null=True)
    step_name = models.CharField(max_length=20, blank=True, null=True)
    wo_qty = models.IntegerField(default=0)
    wo_labor_time = models.FloatField(default=0)
    wo_mach_time = models.FloatField(default=0)
    std_qty = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='wo_excel_temp_create_by')  # 建立者

class COOIS_Record(models.Model):
    batch_no = models.CharField(max_length=20, primary_key=True)
    file_name = models.CharField(max_length=50, blank=False, null=False)
    file_url = models.CharField(max_length=50, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='coois_create_by')  # 建立者

class WOMain(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    batch_no = models.CharField(max_length=20, blank=False, null=False)
    plant = models.CharField(max_length=10, blank=False, null=False)
    wo_no = models.CharField(max_length=20, blank=False, null=False)
    item_no = models.CharField(max_length=20, blank=True, null=True)
    spec = models.CharField(max_length=100, blank=False, null=False)
    version = models.IntegerField(default=1)
    enable = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True, editable=True)  # 建立日期
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='wo_main_create_by')  # 建立者


class WODetail(models.Model):
    wo_main = models.ForeignKey(WOMain, related_name='wo_main', on_delete=models.CASCADE)
    work_center = models.CharField(max_length=20, blank=False, null=False)
    cfm_code = models.CharField(max_length=20, blank=True, null=True)
    ctr_code = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    step_no = models.CharField(max_length=20, blank=True, null=True)
    step_code = models.CharField(max_length=20, blank=True, null=True)
    step_name = models.CharField(max_length=20, blank=True, null=True)
    wo_qty = models.IntegerField(default=0)
    wo_labor_time = models.FloatField(default=0)
    wo_mach_time = models.FloatField(default=0)
    std_qty = models.IntegerField(default=0)


class Machine(models.Model):
    step_code = models.CharField(max_length=20, blank=True, null=True)
    step_name = models.CharField(max_length=20, blank=True, null=True)
    mach_code = models.CharField(max_length=20, primary_key=True)
    mach_name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.mach_name


class Record(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    work_center = models.CharField(max_length=20, blank=False, null=False)
    plant = models.CharField(max_length=10, blank=False, null=False)
    wo_no = models.CharField(max_length=20, blank=False, null=False)
    item_no = models.CharField(max_length=20, blank=False, null=False)
    spec = models.CharField(max_length=100, blank=False, null=False)
    emp_no = models.CharField(max_length=30, blank=False, null=False)
    username = models.CharField(max_length=30, blank=False, null=False)
    sap_emp_no = models.CharField(max_length=30, blank=False, null=False)
    cfm_code = models.CharField(max_length=20, blank=False, null=False)
    ctr_code = models.CharField(max_length=20, blank=True, null=True)
    step_no = models.CharField(max_length=20, blank=True, null=True)
    step_code = models.CharField(max_length=20, blank=True, null=True)
    step_name = models.CharField(max_length=20, blank=True, null=True)
    mach = models.ForeignKey(Machine, related_name='record_mach', on_delete=models.DO_NOTHING, blank=True, null=True)
    record_dt = models.CharField(max_length=10, blank=False, null=False)
    labor_time = models.FloatField(default=0)
    mach_time = models.FloatField(default=0)
    good_qty = models.IntegerField(default=0)
    ng_qty = models.IntegerField(default=0)
    comment = models.CharField(max_length=40, blank=True, null=True)
    sap_flag = models.BooleanField(default=False)
    status = models.CharField(max_length=10, blank=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    update_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='record_update_by')

    def get_absolute_url(self):
        return reverse('prod_record_detail_sap_empno', kwargs={'sap_emp_no': self.sap_emp_no})


class WorkType(models.Model):
    type_code = models.CharField(max_length=5, primary_key=True)
    type_name = models.CharField(max_length=30, blank=False, null=False)
    type_name_vi = models.CharField(max_length=30, blank=False, null=False)
    type_name_en = models.CharField(max_length=30, blank=False, null=False)
    create_at = models.DateTimeField(auto_now=True, null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='worktype_create_by')


class Record2(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    emp_no = models.CharField(max_length=30, blank=False, null=False)
    sap_emp_no = models.CharField(max_length=30, blank=False, null=False)
    record_dt = models.CharField(max_length=10, blank=False, null=False)
    work_type = models.ForeignKey(WorkType, related_name='record_work_type', on_delete=models.DO_NOTHING)
    comment = models.CharField(max_length=255, blank=True, null=True)
    labor_time = models.FloatField(default=0)
    create_at = models.DateTimeField(auto_now=True, null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='record2_create_by')
    qty = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('prod_record_detail_sap_empno', kwargs={'sap_emp_no': self.sap_emp_no})


class Consumption(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    plant = models.CharField(max_length=10, blank=False, null=False)
    cfm_code = models.CharField(max_length=20, blank=False, null=False)
    wo_no = models.CharField(max_length=20, blank=False, null=False)
    wo_mtrl_no = models.CharField(max_length=20, blank=False, null=False)
    item_no = models.CharField(max_length=20, blank=False, null=False)
    qty = models.FloatField(default=0)
    sap_flag = models.BooleanField(default=False)
    create_at = models.DateTimeField(auto_now=True, null=True)
    create_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING,
                                  related_name='consumption_create_by')

class Sync_SAP_Log(models.Model):
    function = models.CharField(max_length=20, blank=False, null=False)
    batch_no = models.CharField(max_length=20, blank=False, null=False)
    file_name = models.CharField(max_length=30, blank=True, null=True)
    amount = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now=True, null=True)
    create_by = models.CharField(max_length=20)


class Series(models.Model):
    function = models.CharField(max_length=20)
    key = models.CharField(max_length=20)
    series = models.IntegerField()

    class Meta:
        unique_together = (("function", "key"),)
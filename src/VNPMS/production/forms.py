from datetime import datetime, timedelta
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Button
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils.translation import gettext_lazy as _
from production.models import Record, Machine


class ExportForm(forms.Form):
    plant = forms.ChoiceField(label="廠別", choices=(('', '-------'), ('302A', '302A'), ('302B', '302B'),), required=True, initial='')

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('plant', css_class='col-md-9'),
                Div(Submit('submit', _('export'), css_class='btn btn-info'),
                    css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


class WoSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('wo_no',)

    wo_no = forms.CharField(label=_('prod_order'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('wo_no', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


class ItemSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('item_no', 'start_date', 'due_date')

    item_no = forms.CharField(label=_('item_no'))
    start_date = forms.DateField(label="日期(起)")
    due_date = forms.DateField(label="日期(迄)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-3'),
                Div('due_date', css_class='col-md-3'),
                Div('item_no', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': (datetime.now() - timedelta(days=45)).strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

        self.fields['due_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class RecordSearchForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('sap_emp_no', 'record_dt',)

    sap_emp_no = forms.CharField(required=True, label=_('sap_emp_no'))
    record_dt = forms.DateField(label=_('record_date'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('sap_emp_no', css_class='col-md-3'),
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('worked_labor_time', 'record_dt', 'plant', 'wo_no', 'item_no', 'spec', 'emp_no', 'username', 'sap_emp_no', 'step_code', 'step_name', 'cfm_code',
                  'labor_time', 'mach_time', 'good_qty', 'ng_qty', 'ctr_code', 'comment', 'step_no', 'work_center')

    record_dt = forms.DateField(label=_('record_date'))
    worked_labor_time = forms.DateField(required=False, label=_('worked_labor_time'))
    plant = forms.CharField(required=True, label=_('plant'))
    wo_no = forms.CharField(required=True, label=_('prod_order'))
    item_no = forms.CharField(required=True, label=_('item_no'))
    spec = forms.CharField(required=True, label=_('spec'))
    emp_no = forms.CharField(required=False, label=_('emp_no'))
    username = forms.CharField(required=False, label=_('name'))
    sap_emp_no = forms.CharField(required=True, label=_('sap_emp_no'))
    cfm_code = forms.CharField(required=True, label=_('confirm_code'))
    ctr_code = forms.CharField(required=True, label=_('control_code'))
    step_code = forms.CharField(required=False, label=_('step_code'))
    step_name = forms.CharField(required=False, label=_('step_name'), widget=forms.TextInput(attrs={'class': 'text-light bg-dark'}))
    labor_time = forms.CharField(required=True, label=_('labor_time'))
    mach_time = forms.CharField(required=False, label=_('mach_time'))
    good_qty = forms.IntegerField(required=True, label=_('good_qty'))
    ng_qty = forms.IntegerField(required=True, label=_('ng_qty'), initial=0)
    comment = forms.CharField(required=False, label=_('comment'), max_length=40)
    step_no = forms.CharField(required=True)
    work_center = forms.CharField(required=True)
    mach_code = forms.ModelChoiceField(required=False, label=_('mach_name'), queryset=Machine.objects.none())
    status = forms.ChoiceField(label="確認類型", choices=(('X', '最後確認'), ('', '部分確認'),), required=True)

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['plant'].widget.attrs['readonly'] = True
        self.fields['wo_no'].widget.attrs['readonly'] = True
        self.fields['item_no'].widget.attrs['readonly'] = True
        self.fields['spec'].widget.attrs['readonly'] = True
        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['emp_no'].widget.attrs['readonly'] = True
        self.fields['step_code'].widget.attrs['readonly'] = True
        self.fields['step_name'].widget.attrs['readonly'] = True
        self.fields['ctr_code'].widget.attrs['readonly'] = True
        self.fields['worked_labor_time'].widget.attrs['readonly'] = True
        self.fields['step_no'].widget = forms.HiddenInput()
        self.fields['work_center'].widget = forms.HiddenInput()
        self.fields['status'].initial = 'X'

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('sap_emp_no', css_class='col-md-3'),
                Div('username', css_class='col-md-3'),
                Div('emp_no', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('record_dt', css_class='col-md-3'),
                Div('worked_labor_time', css_class='col-md-3'),
                Div(Button('mtr_change', '物料異動', onclick='popup()', css_class='btn btn-info m-3'), css_class='col-md-3'),
                Div('status', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('plant', css_class='col-md-3'),
                Div('wo_no', css_class='col-md-3'),
                Div('item_no', css_class='col-md-3'),
                Div('spec', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('cfm_code', css_class='col-md-3'),
                Div('step_code', css_class='col-md-3'),
                Div('step_name', css_class='col-md-3'),
                Div('ctr_code', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('good_qty', css_class='col-md-3'),
                Div('ng_qty', css_class='col-md-3'),
                Div('comment', css_class='col-md-6'),
                css_class='row'),
            Div(
                Div('mach_time', css_class='col-md-3'),
                Div('labor_time', css_class='col-md-3'),
                Div('mach_code', css_class='col-md-3'),
                css_class='row'),
            Div(Submit('submit', _('save'), css_class='btn btn-info m-3'),
                css_class='row'),
            Div(
                Div('step_no', css_class='col-md-2'),
                Div('work_center', css_class='col-md-2'),
                css_class='row'),
        )


        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class RecordManageForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('record_dt',)

    record_dt = forms.DateField(label=_('record_date'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('record_dt', css_class='col-md-3'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )


        self.fields['record_dt'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class RecordHistoryForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ('start_date', 'due_date',)

    start_date = forms.DateField(label="日期(起)")
    due_date = forms.DateField(label="日期(迄)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-3'),
                Div('due_date', css_class='col-md-3'),
                Div(Submit('submit', _('export'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center mt-3'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': (datetime.now()-timedelta(days=45)).strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

        self.fields['due_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )
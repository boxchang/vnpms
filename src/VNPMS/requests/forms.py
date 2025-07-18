from bootstrap_datepicker_plus.widgets import DatePickerInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML
from django import forms
from django.utils.translation import gettext_lazy as _
from bases.models import Status
from requests.models import Request, Level, Request_reply
from datetime import datetime, timedelta
from users.models import CustomUser
from projects.models import Project
from django_select2 import forms as s2forms

class RequestHistoryForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ('status', 'owner', 'plant', 'start_date', 'due_date',)

    status = forms.ModelChoiceField(required=False, label=_(
        'status'), queryset=Status.objects.all(), initial=1)
    owner = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        required=False,
        label=_('Owner'),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    plant = forms.ChoiceField(required=False, label=_("Plant"),
                              choices=[('', '---------'), ('GD', 'GD'), ('LK', 'LK'), ('LT', 'LT')])
    start_date = forms.DateField(label=_("Creation Date (From)"))
    due_date = forms.DateField(label=_("Creation Date (To)"))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-2'),
                Div('due_date', css_class='col-md-2'),
                Div('plant', css_class='col-md-2'),
                Div('owner', css_class='col-md-2'),
                Div('status', css_class='col-md-2'),
                Div(Submit('submit', _('search'), css_class='btn btn-info'),
                    css_class='col-md-2 p-0 d-flex align-items-center', style='height: 100px;'),
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

class RequestReceiveForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            'start_date', 'due_date', 'estimate_time'
        )
        estimate_time = forms.IntegerField(required=False, label=_('estimate_time'), widget=forms.NumberInput(),
                                           initial=0, )
        start_date = forms.DateField(label=_('starttime'))
        due_date = forms.DateField(label=_('finishtime'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-6'),
                Div('due_date', css_class='col-md-6'),
                css_class='row'),
            Div('estimate_time'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).start_of('request days')

        self.fields['due_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        ).end_of('request days')

    # def clean_due_date(self):
    #     if self.cleaned_data['start_date'] <= self.cleaned_data['due_date']:
    #         return self.cleaned_data['due_date']
    #     else:
    #         raise forms.ValidationError(u"預計完成日期不能小於開始日期")

class RequestReplyForm(forms.ModelForm):
    class Meta:
        model = Request_reply
        fields = ('desc',)

        desc = forms.CharField(required=False, widget=CKEditorUploadingWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.fields['desc'].label = ""
        self.helper.layout = Layout(
            Div(
                Div('desc', css_class='col-12'),
                css_class='row'
            )
        )


class ProjectWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'name__icontains',
    ]


class BelongToWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        'title__icontains',
    ]


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = (
            'title', 'start_date', 'due_date', 'process_rate', 'estimate_time', 'level', 'plant', 'owner', 'desc',
            'status', 'actual_date', 'project', 'belong_to',)

    level = forms.ModelChoiceField(required=True, label=_('level'), queryset=Level.objects.all(), initial=2)
    plant = forms.ChoiceField(required=False, label=_("Plant"),
                              choices=[('', '---'), ('GD', 'GD'), ('LK', 'LK'), ('LT', 'LT')])
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget())
    status = forms.ModelChoiceField(required=True, label=_('status'), queryset=Status.objects.all(), initial=1)
    owner = forms.ModelChoiceField(
        required=False,
        label=_('owner'),
        queryset=CustomUser.objects.all(),
        widget=s2forms.Select2Widget(attrs={
            'class': 'form-control select-field',
            'data-placeholder': _('Search owner...'),
            'data-minimum-input-length': 0,
        })
    )
    estimate_time = forms.IntegerField(required=False, label=_('estimate_time'), widget=forms.NumberInput(), initial=0, )
    start_date = forms.DateField(label=_('starttime'))
    due_date = forms.DateField(label=_('finishtime'))
    actual_date = forms.DateField(required=False, label=_('actualtime'))
    project = forms.ModelChoiceField(
        required=False,
        queryset=Project.objects.all(),
        label=_('project'),
        widget=s2forms.Select2Widget(attrs={
            'class': 'form-control select-field',
            'data-placeholder': _('Search project...'),
            'data-minimum-input-length': 0,
        })
    )
    belong_to = forms.ModelChoiceField(
        required=False,
        queryset=Request.objects.filter(status_id__in=[1, 2]),
        label=_('belong_to'),
        widget=s2forms.Select2Widget(attrs={
            'class': 'form-control select-field',
            'data-placeholder': _('Search request...'),
            'data-minimum-input-length': 0,
        })
    )

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('level', css_class='col-md-6'),
                Div('status', css_class='col-md-6'),
                css_class='row'),
            Div(
                Div('plant', css_class='col-md-3'),
                Div('title', css_class='col-md-9'),
                css_class='row'),
            Div('desc'),
            Div('actual_date'),
            Div(Div('start_date', css_class='col-md-6'),
                Div('due_date', css_class='col-md-6'),
                css_class='row'),
            Div(Div('owner', css_class='col-md-6'),
                Div('estimate_time', css_class='col-md-6'),
                css_class='row'),
            Div(Div('project', css_class='col-md-6'),
                Div('belong_to', css_class='col-md-6'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
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

        self.fields['actual_date'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )

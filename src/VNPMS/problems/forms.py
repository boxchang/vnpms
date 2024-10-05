from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Button
from django import forms
from datetime import datetime, timedelta
from bases.models import Status
from problems.models import Problem, Problem_reply, ProblemType
from users.models import Unit
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils import timezone


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('problem_type', 'problem_status', 'title', 'desc', 'requester', 'problem_datetime', 'plant', 'dept')

    problem_type = forms.ModelChoiceField(required=False, label="問題類型", queryset=ProblemType.objects.all(), empty_label="---")
    problem_status = forms.ModelChoiceField(required=False, label="問題狀態", queryset=Status.objects.all(), initial=1)
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget())
    problem_datetime = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label="Problem Datetime")
    requester = forms.CharField(required=True, label=_('Requester'))
    plant = forms.ChoiceField(required=False, label="Plant", choices=[('', '---'), ('NBR', 'NBR'), ('PVC', 'PVC')])
    dept = forms.ChoiceField(required=True, label="Dept.", choices=[(unit.unitId, unit.unitName) for unit in Unit.objects.all()])
    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.fields['problem_datetime'].initial = timezone.now

        if not self.instance.pk:
            self['desc'].initial = """
            【問題描述】<p \>
            【問題原因】<p \>
            【Short-Term Solution】<p \>
            【Long-Term Solution】<p \>
            """

        self.helper.layout = Layout(
            Div(
                Div('problem_type', css_class='col-md-3'),
                Div('problem_status', css_class='col-md-3'),
                Div('requester', css_class='col-md-3'),
                Div('problem_datetime', css_class='col-md-3'),
                Div('plant', css_class='col-md-3'),
                Div('dept', css_class='col-md-3'),
                Div('title', css_class='col-md-6'),
                css_class='row'),
            Div('desc'),
        )


class ProblemReplyForm(forms.ModelForm):
    class Meta:
        model = Problem_reply
        fields = ('comment', )

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False

    comment = forms.CharField(
        required=True, label='', widget=CKEditorUploadingWidget())


class ProblemHistoryForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('status', 'start_date', 'due_date',)

    status = forms.ModelChoiceField(required=False, label=_(
        'status'), queryset=Status.objects.all(), initial=1)
    problem_type = forms.ModelChoiceField(required=False, label="問題類型", queryset=ProblemType.objects.all(),
                                          empty_label="---")
    start_date = forms.DateField(label="建立日期(起)")
    due_date = forms.DateField(label="建立日期(迄)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-2'),
                Div('due_date', css_class='col-md-2'),
                Div('problem_type', css_class='col-md-2'),
                Div('status', css_class='col-md-2'),
                Div(Submit('submit', '查詢', css_class='btn btn-info'), css_class='col-md-2 d-flex align-items-center'),
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

class ProblemChartForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ('status', 'start_date',)

    status = forms.ModelChoiceField(required=False, label=_(
        'status'), queryset=Status.objects.all(), initial=0)
    start_date = forms.DateField(label="建立日期(起)")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-3'),
                Div('status', css_class='col-md-3'),
                Div(Button('search', '查詢', css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center search_btn_fix'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
                attrs={'value': datetime.now().strftime('%Y-%m-%d')},
                options={
                    "format": "YYYY-MM",
                    "showClose": False,
                    "showClear": False,
                    "showTodayButton": False,
                }
            )

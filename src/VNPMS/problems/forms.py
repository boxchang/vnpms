from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, Button, HTML
from django import forms
from datetime import datetime, timedelta
from bases.models import Status
from problems.models import Problem, Problem_reply, ProblemType
from users.models import Unit, CustomUser, Plant, UserType
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django.utils import timezone
from django_select2 import forms as s2forms


class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = (
        'problem_type', 'problem_status', 'title', 'desc', 'requester', 'problem_datetime', 'expected_datetime',
        'finish_datetime', 'root_cause', 'short_term', 'long_term', 'plant', 'dept', 'owner')

    problem_type = forms.ModelChoiceField(required=True, label=_("Problem Type"), queryset=ProblemType.objects.all(),
                                          empty_label="---")
    problem_status = forms.ModelChoiceField(required=False, label=_("status"), queryset=Status.objects.all(), initial=6)
    title = forms.CharField(required=True, label=_('title'))
    desc = forms.CharField(required=False, label=_('desc'), widget=CKEditorUploadingWidget(config_name='default'))
    root_cause = forms.CharField(required=False, label=_('Root Cause'),
                                 widget=CKEditorUploadingWidget(config_name='default'))
    short_term = forms.CharField(required=False, label=_('Short Term Solution'),
                                 widget=CKEditorUploadingWidget(config_name='default'))
    long_term = forms.CharField(required=False, label=_('Long Term Solution'),
                                widget=CKEditorUploadingWidget(config_name='default'))
    problem_datetime = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        label=_("Problem Datetime"))
    expected_datetime = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        label=_("Expected Datetime"))
    finish_datetime = forms.DateTimeField(widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        label=_("Finish Datetime"))
    requester = forms.CharField(required=True, label=_('Requester'))
    plant = forms.ModelChoiceField(
        required=True,
        label=_("Plant"),
        queryset=Plant.objects.all(),
        empty_label='---',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    dept = forms.ModelChoiceField(
        required=True,
        label=_("Dept."),
        queryset=Unit.objects.all(),
        empty_label='--------',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    owner = forms.ModelChoiceField(
        label=_('Issue Owner'),
        queryset=CustomUser.objects.all(),
        widget=s2forms.Select2Widget(attrs={
            'class': 'form-control select-field',
            'data-placeholder': _('Search owner...'),
            'data-minimum-input-length': 0,
        }),
    )

    def __init__(self, *args, submit_title='Submit', project=None, user=None, members=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        if members is not None:
            if self.instance and self.instance.owner and self.instance.owner not in members:
                members = members | CustomUser.objects.filter(pk=self.instance.owner.pk)
            self.fields['owner'].queryset = members

        if self.instance and self.instance.pk:
            self.fields['owner'].initial = self.instance.owner

        self.user = user
        user_type_requester = UserType.objects.get(type_name='Requester')

        if user:
            if user.user_type == user_type_requester:
                self.fields['owner'].disabled = True
                self.fields['problem_status'].disabled = True

            self.fields['requester'].initial = user.username
            if user.unit:
                self.initial['dept'] = user.unit

                plant = Plant.objects.get(pk=user.unit.plant_id)
                self.initial['plant'] = plant

        self.fields['problem_datetime'].initial = timezone.now

        self.fields['expected_datetime'].required = False
        self.fields['finish_datetime'].required = False
        self.fields['owner'].required = False
        self.fields['problem_type'].required = False
        self.fields['owner'].initial = None

        # if not self.instance.pk:
        #     self['desc'].initial = """
        #     【Problem Description】<p \>
        #     【Problem Root Cause】<p \>
        #     【Short-Term Solution】<p \>
        #     【Long-Term Solution】<p \>
        #     """

        if project and project.belong_to:
            self.fields['problem_type'].queryset = ProblemType.objects.filter(belong_to=project.belong_to)
        else:
            self.fields['problem_type'].queryset = ProblemType.objects.none()

        #self.fields['dept'].disabled = True  # default

        plant = self.instance.plant
        if plant:
            self.initial['plant'] = plant
        elif self.instance and self.instance.plant:
            if str(self.instance.plant).isdigit():
                self.initial['plant'] = str(self.instance.plant)
            else:
                plant = Plant.objects.get(plant_code=self.instance.plant)
                self.initial['plant'] = '1'

        dept = self.instance.dept
        if dept:
            self.initial['dept'] = dept
            #self.fields['dept'].disabled = False

        # if 'plant' in self.data:
        #     units = Unit.objects.filter(plant_id=self.data['plant'])
        #     self.fields['dept'].choices = [(unit.id, unit.unitName) for unit in units]
        #     self.fields['dept'].disabled = False
        #
        #     # Set initial dept
        #     if 'dept' in self.data:
        #         self.initial['dept'] = self.data['dept']
        # else:
        #     self.fields['dept'].choices = [('', '---------')]
        #     self.fields['dept'].disabled = True

        # self.helper.layout = Layout(
        #     Div(
        #         Div('problem_type', css_class='col-md-3'),
        #         Div('problem_status', css_class='col-md-3'),
        #         Div('owner', css_class='col-md-3'),
        #         Div('problem_datetime', css_class='col-md-3'),
        #         Div('plant', css_class='col-md-3'),
        #         Div('dept', css_class='col-md-3'),
        #         Div('requester', css_class='col-md-3'),
        #         Div('title', css_class='col-md-12'),
        #         css_class='row'),
        #     Div('desc'),
        # )

        self.helper.layout = Layout(
            # Part 1: Basic Information
            Div(
                HTML(f'<h5 class="text-center font-weight-bold">{_("Basic Information")}</h5>'),
                css_class='card-header bg-transparent'
            ),
            Div(
                Div(
                    Div('problem_datetime', css_class='col-md-4'),
                    Div('expected_datetime', css_class='col-md-4'),
                    css_class='row mb-3'
                ),
                Div(
                    Div('plant', css_class='col-md-4'),
                    Div('dept', css_class='col-md-4'),
                    Div('requester', css_class='col-md-4'),
                    css_class='row mb-3'
                ),
                Div(
                    Div('title', css_class='col-md-12'),
                    css_class='row mb-3'
                ),
                Div('desc'),
                css_class='card-body'
            ),
        )
        if self.instance.id and user.user_type.type_name != 'Requester':
            # self.fields['problem_type'].required = True

            self.helper.layout = Layout(
                # Part 1: Basic Information
                Div(
                    HTML(f'<h5 class="text-center font-weight-bold">{_("Basic Information")}</h5>'),
                    css_class='card-header bg-transparent'
                ),
                Div(
                    Div(
                        Div('problem_datetime', css_class='col-md-3'),
                        Div('expected_datetime', css_class='col-md-3'),
                        Div('owner', css_class='col-md-3'),
                        Div('problem_status', css_class='col-md-3'),
                        css_class='row mb-3'
                    ),
                    Div(
                        Div('plant', css_class='col-md-3'),
                        Div('dept', css_class='col-md-3'),
                        Div('requester', css_class='col-md-3'),
                        css_class='row mb-3'
                    ),
                    Div(
                        Div('title', css_class='col-md-12'),
                        css_class='row mb-3'
                    ),
                    Div('desc'),
                    css_class='card-body'
                ),

                # Part 2: Problem details
                Div(
                    HTML(f'<h5 class="text-center font-weight-bold">{_("Problem Detail")}</h5>'),
                    css_class='card-header bg-transparent'
                ),
                Div(
                    Div(
                        Div('problem_type', css_class='col-md-3'),
                        Div('finish_datetime', css_class='col-md-3'),
                        css_class='row mb-3'
                    ),
                    Div(
                        Div('root_cause', css_class='col-md-12'),
                        css_class='row mb-3'
                    ),
                    Div(
                        Div('short_term', css_class='col-md-12'),
                        css_class='row mb-3'
                    ),
                    Div(
                        Div('long_term', css_class='col-md-12'),
                        css_class='row mb-3'
                    ),
                    css_class='card-body'
                )
            )

    def clean_owner(self):
        owner = self.cleaned_data.get('owner')
        if owner == '':
            return None
        return owner


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
        fields = ('problem_type', 'owner', 'problem_status', 'start_date', 'due_date',)

    problem_status = forms.ModelChoiceField(required=False, label=_('Status'), queryset=Status.objects.all(), initial=1)
    problem_type = forms.ModelChoiceField(required=False, label=_("Question Type"), queryset=ProblemType.objects.all(),
                                          empty_label="---")
    owner = forms.ModelChoiceField(required=False, label=_("Issue Owner"), queryset=CustomUser.objects.all(),
                                          empty_label="---")
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
                Div('problem_type', css_class='col-md-2'),
                Div('owner', css_class='col-md-2'),
                Div('problem_status', css_class='col-md-2'),
                Div(Submit('submit', _('search'),
                           css_class='btn btn-info'),
                    css_class='col-md-2 p-0 d-flex align-items-center', style='height: 100px;'),
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
    start_date = forms.DateField(label=_("Creation Date (From)"))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-3'),
                Div('status', css_class='col-md-3'),
                Div(Button('search', _('search'), css_class='btn btn-info'), css_class='col-md-3 d-flex align-items-center search_btn_fix'),
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



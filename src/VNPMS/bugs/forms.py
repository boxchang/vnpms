from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from django.utils.translation import gettext_lazy as _
from bases.models import Status
from bugs.models import Bug
from projects.models import Project
from requests.models import Level, Request
from users.models import CustomUser


class BugForm(forms.ModelForm):
    class Meta:
        model = Bug
        fields = ('title', 'level', 'status', 'owner', 'desc', 'belong_to')

    title = forms.CharField(required=True, label=_('title'))
    level = forms.ModelChoiceField(required=True, label=_(
        'level'), queryset=Level.objects.all(), initial=2)  # initial MEDIUM
    status = forms.ModelChoiceField(required=True, label=_(
        'status'), queryset=Status.objects.all(), initial=1)
    owner = forms.ModelChoiceField(required=False, label=_(
        'owner'), queryset=CustomUser.objects.all())
    belong_to = forms.ModelChoiceField(required=False, label=_(
        'belong_to'), queryset=Request.objects.all())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        # if submit_title:
        #     self.helper.add_input(Submit('submit', submit_title))
        self.helper.layout = Layout(
            Div('title'),
            Div(Div('level', css_class='col-md-6'),
                Div('owner', css_class='col-md-6'),
                css_class='row'),
            Div('desc'),
            Div('status'),
        )

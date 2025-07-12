from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div
from django import forms
from helpdesk.models import Helpdesk, HelpdeskType
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.translation import gettext_lazy as _


class HelpdeskForm(forms.ModelForm):
    class Meta:
        model = Helpdesk
        fields = ('help_type', 'title', 'desc')

    help_type = forms.ModelChoiceField(
        required=True, label=_("Document type"), queryset=HelpdeskType.objects.all())
    title = forms.CharField(required=True, label=_("Title"))
    desc = forms.CharField(required=False, label=_("Describe"),
                           widget=CKEditorUploadingWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div('help_type'),
            Div('title'),
            Div('desc')
        )

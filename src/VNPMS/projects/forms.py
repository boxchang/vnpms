from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from django import forms
from django.core.validators import RegexValidator
from django.forms import CheckboxSelectMultiple
from django.utils.translation import gettext_lazy as _
from projects.models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'short_name', 'desc',)

    alphanumeric = RegexValidator(r'^[A-Z]*$', _('alphanumeric'))

    name = forms.CharField(required=True, label=_(
        'name'), help_text=_('help_name'))
    short_name = forms.CharField(required=True, max_length=3, label=_('short_name'), help_text=_('help_short'),
                                 validators=[alphanumeric])
    desc = forms.CharField(required=True, label=_('desc'), help_text=_(
        'help_desc'), widget=CKEditorUploadingWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['short_name'].widget.attrs['style'] = 'width:100px;'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        # if submit_title:
        #     self.helper.add_input(Submit('submit', submit_title))


class ProjectSettingForm(forms.ModelForm):
    class Meta:
        model = Project_setting
        fields = ('project', 'default', 'page_number')

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        # self.fields["project"].widget = CheckboxSelectMultiple(
        #     attrs={"checked": ""})  # 下拉選項改成核取方塊


    def clean_default(self):
        default = self.cleaned_data['default']
        project = self.cleaned_data['project']
        if default in project:
            return default
        else:
            raise forms.ValidationError(u"預設專案必須被選擇")

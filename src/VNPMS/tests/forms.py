from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML
from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from tests.models import Request_test, Request_test_item


class RTestForm(forms.ModelForm):
    class Meta:
        model = Request_test
        fields = ('desc',)
    desc = forms.CharField(required=True, label=_(
        'desc'), widget=CKEditorUploadingWidget(config_name='special'))

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True
        self.helper.layout = Layout(
            Div('desc'),
        )


BaseTestItemFormSet = inlineformset_factory(
    parent_model=Request_test, model=Request_test_item, fields=('item',), extra=2
)


class RTestItemFormSet(BaseTestItemFormSet):

    def add_fields(self, form, index):
        super(RTestItemFormSet, self).add_fields(form, index)
        form.fields['item'] = forms.CharField(
            label='', required=True, widget=forms.TextInput())
        form.fields['DELETE'].label = ''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            HTML("{% if forloop.first %}"
                 "<div class='row'>"
                 "<div class='col-md-6 text-muted'>item</div>"
                 "<div class='col-md-2'>delete</div>"
                 "</div>"
                 "{% endif %}"),
            Div(Div('item', css_class='col-md-6'),
                Div('DELETE', css_class='col-md-2'),
                css_class='row'),
        )

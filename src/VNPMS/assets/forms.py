from django import forms
from .models import Asset, AssetCategory, AssetType, Brand, Location, AssetArea, AssetStatus, Unit
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Fieldset
from bootstrap_datepicker_plus.widgets import DatePickerInput
from datetime import datetime
from django.core.validators import RegexValidator
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class AssetSearchForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = (
            'label_no', 'status', 'category', 'type', 'brand', 'area', 'location')

    label_no = forms.CharField(required=False, label="標籤編號(包含SAP資產編號)")
    category = forms.ModelChoiceField(required=False, label="資產類別", queryset=AssetCategory.objects.all())
    type = forms.ModelChoiceField(required=False, label="資產種類", queryset=AssetType.objects.all())
    brand = forms.ModelChoiceField(required=False, label="品牌", queryset=Brand.objects.all())
    area = forms.ModelChoiceField(required=False, label="地區", queryset=AssetArea.objects.all())
    location = forms.ModelChoiceField(required=False, label="放置地點", queryset=Location.objects.all())
    status = forms.ModelChoiceField(required=False, label="狀態", queryset=AssetStatus.objects.all())
    scrap = forms.BooleanField(required=False, initial=False, label="包含報廢")
    show_sap_no = forms.BooleanField(required=False, initial=False, label="顯示SAP產編")
    location_desc = forms.CharField(required=False, label="放置地點描述")
    keeper_unit = forms.ModelChoiceField(required=False, label="保管單位", queryset=Unit.objects.all())
    keeper_name = forms.CharField(required=False, label="保管人姓名")
    desc = forms.CharField(required=False, label="關鍵字查詢")

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Fieldset('Search Condition',
                Div(
                    Div('label_no', css_class='col-md-4'),
                    Div('status', css_class='col-md-4'),
                    Div('scrap', css_class='col-md-2'),
                    Div('show_sap_no', css_class='col-md-2'),
                    css_class='row'),
                Div(
                    Div('category', css_class='col-md-4'),
                    Div('type', css_class='col-md-4'),
                    Div('brand', css_class='col-md-4'),
                    css_class='row'),
                Div(
                    Div('area', css_class='col-md-4'),
                    Div('location', css_class='col-md-4'),
                    Div('location_desc', css_class='col-md-4'),
                    css_class='row'),
                Div(
                    Div('keeper_unit', css_class='col-md-4'),
                    Div('keeper_name', css_class='col-md-4'),
                    Div('desc', css_class='col-md-4'),
                    css_class='row'),
            )
        )


class AssetModelForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('label_no', 'auto_encode', 'category', 'type', 'brand', 'model', 'desc', 'owner_unit', 'keeper_unit',
            'keeper_name', 'location', 'location_desc', 'pur_date', 'pur_price', 'area', 'status', 'comment',
                  'scrap_date', 'scrap_reason', 'sap_asset_no')

    label_no = forms.CharField(required=False, label="標籤編號")
    auto_encode = forms.BooleanField(required=False, initial=True, label="自動編碼")
    pur_price = forms.IntegerField(required=True, label="採購金額", widget=forms.NumberInput(), initial=0)
    pur_date = forms.CharField(required=False, label="採購年月")
    category = forms.ModelChoiceField(required=True, label="資產類別", queryset=AssetCategory.objects.all())
    type = forms.ModelChoiceField(required=True, label="資產種類", queryset=AssetType.objects.all())
    brand = forms.ModelChoiceField(required=True, label="品牌", queryset=Brand.objects.all())
    model = forms.CharField(required=False, initial="", label="型號")
    desc = forms.CharField(required=False, initial="", label="描述")
    area = forms.ModelChoiceField(required=True, label="地區", queryset=AssetArea.objects.all())
    owner_unit = forms.ModelChoiceField(required=True, label="負責單位", queryset=Unit.objects.all())
    keeper_unit = forms.ModelChoiceField(required=False, initial="", label="保管單位", queryset=Unit.objects.all())
    keeper_name = forms.CharField(required=False, initial="", label="保管人姓名")
    location = forms.ModelChoiceField(required=True, label="放置地點", queryset=Location.objects.all())
    location_desc = forms.CharField(required=False, label="放置地點描述")
    status = forms.ModelChoiceField(required=True, label="狀態", queryset=AssetStatus.objects.all())
    sap_asset_no = forms.CharField(required=False, initial="", label="SAP資產編號")
    scrap_date = forms.CharField(required=False, initial="", label="報廢日期")
    scrap_reason = forms.CharField(required=False, initial="", label="報廢原因")
    comment = forms.CharField(required=False, label="備註", widget=CKEditorUploadingWidget())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label_no'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Fieldset('Main Data',
                Div(
                    Div('label_no', css_class='col-md-4'),
                    Div('auto_encode', css_class='col-md-4'),
                    Div('status', css_class='col-md-4'),
                    css_class='row'),
                Div(
                    Div('category', css_class='col-md-4'),
                    Div('type', css_class='col-md-4'),
                    Div('brand', css_class='col-md-4'),
                    css_class='row'),
                Div(
                    Div('model', css_class='col-md-6'),
                    Div('desc', css_class='col-md-6'),
                    css_class='row'),
            ),
            HTML('<hr>'),
            Fieldset('Owner & Location',
                Div(
                    Div('area', css_class='col-md-4'),
                    Div('location', css_class='col-md-4'),
                    Div('location_desc', css_class='col-md-4'),
                    css_class='row'),
                Div(
                    Div('owner_unit', css_class='col-md-4'),
                    Div('keeper_unit', css_class='col-md-4'),
                    Div('keeper_name', css_class='col-md-4'),
                    css_class='row'),
            ),
            HTML('<hr>'),
            Fieldset('Procurement',
                Div(
                    Div('pur_date', css_class='col-md-4'),
                    Div('pur_price', css_class='col-md-4'),
                    Div('sap_asset_no', css_class='col-md-4'),
                    css_class='row'),
                Div(
                    Div('scrap_date', css_class='col-md-4'),
                    Div('scrap_reason', css_class='col-md-4'),
                    css_class='row'),
            ),
            HTML('<hr>'),
            Div(
                Div('comment', css_class='col-md-12'),
                css_class='row'),
        )

        self.fields['pur_date'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM",
                "showClose": False,
                "showClear": True,
                "showTodayButton": False,
            }
        )

        self.fields['scrap_date'].widget = DatePickerInput(
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": True,
                "showTodayButton": False,
            }
        )

    def clean_pur_date(self):
        value = self.cleaned_data['pur_date'][0:7]
        return value


class CategoryResetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ('category',)

    category = forms.ModelChoiceField(required=False, label="資產類別", queryset=AssetCategory.objects.all())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('category', css_class='col-md-12'),
                css_class='row'),
        )
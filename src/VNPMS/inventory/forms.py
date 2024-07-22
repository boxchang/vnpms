from datetime import datetime, timedelta
from django import forms
from users.models import Unit, CustomUser
from .models import AppliedForm, ItemType, Item, AppliedItem, ItemCategory, FormStatus, ItemFamily
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, HTML, Button, Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput


class InvAppliedHistoryForm(forms.ModelForm):
    class Meta:
        model = AppliedForm
        fields = ('status', 'start_date', 'due_date',)

    status = forms.ModelChoiceField(required=False, label="狀態", queryset=FormStatus.objects.all(), initial=0)
    start_date = forms.DateField(label="申請日期(起)")
    due_date = forms.DateField(label="申請日期(迄)")
    category = forms.ModelChoiceField(required=False, label="物品類別", queryset=ItemCategory.objects.all(), initial=0)
    unit = forms.ModelChoiceField(required=False, label="申請部門", queryset=Unit.objects.all(),
                                  widget=forms.Select(attrs={"onChange": "dept_change()"}))
    requester = forms.ModelChoiceField(required=False, label="申請人/代申請人/簽核者", queryset=CustomUser.objects.none())

    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(Div('start_date', css_class='col-md-2'),
                Div('due_date', css_class='col-md-2'),
                Div('status', css_class='col-md-2'),
                css_class='row'),
            Div(Div('category', css_class='col-md-2'),
                Div('unit', css_class='col-md-2'),
                Div('requester', css_class='col-md-2'),
                Div(Button('search', '查詢', css_class='btn btn-info', onclick="submit1();"), css_class='col-md-3 d-flex align-items-center'),
                Div(Button('export', 'Excel', css_class='btn btn-info', onclick="export_excel();"),
                    css_class='col-md-3 d-flex align-items-center'),
                css_class='row'),
        )

        self.fields['start_date'].widget = DatePickerInput(
            attrs={'value': (datetime.now()-timedelta(days=60)).strftime('%Y-%m-%d')},
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


class SearchForm(forms.Form):
    category = forms.ModelChoiceField(required=False, label="物品類別", queryset=ItemCategory.objects.all(), to_field_name="catogory_code")
    type = forms.ModelChoiceField(required=False, label="物品種類", queryset=ItemType.objects.none())
    keyword = forms.CharField(required=False, label="關鍵字")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('category', css_class='col-md-4'),
                Div('type', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('keyword', css_class='col-md-10'),
                Div(Button('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-2 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


class OfficeInvForm(forms.ModelForm):
    class Meta:
        model = AppliedForm
        fields = ('unit', 'requester', 'apply_date', 'ext_number', 'reason')

    reason = forms.CharField(required=True, label="原因", widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))
    unit = forms.ModelChoiceField(required=True, label="申請部門", queryset=Unit.objects.all(), widget=forms.Select(attrs={"onChange": "dept_change()"}))
    requester = forms.ModelChoiceField(required=True, label="申請人", queryset=CustomUser.objects.none())
    apply_date = forms.CharField(required=True, label="申請日期")
    ext_number = forms.CharField(required=True, label="分機")
    category = forms.ModelChoiceField(required=False, label="物品類別", queryset=ItemCategory.objects.all())
    type = forms.ModelChoiceField(required=False, label="物品種類", queryset=ItemType.objects.all())
    item = forms.ModelChoiceField(required=False, label="物品", queryset=Item.objects.all())
    item_qty = forms.IntegerField(required=False, label="數量")
    keyword = forms.CharField(required=False, label="關鍵字")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('unit', css_class='col-md-3'),
                Div('requester', css_class='col-md-3'),
                Div('ext_number', css_class='col-md-3'),
                Div('apply_date', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('reason', css_class='col-md-12'),
                css_class='row'),
        )

        self.fields['apply_date'].widget = DatePickerInput(
            attrs={'value': datetime.now().strftime('%Y-%m-%d')},
            options={
                "format": "YYYY-MM-DD",
                "showClose": False,
                "showClear": False,
                "showTodayButton": False,
            }
        )


class AttachmentForm(forms.Form):
    file1 = forms.FileField(required=False, label="附件1")
    file2 = forms.FileField(required=False, label="附件2")
    file3 = forms.FileField(required=False, label="附件3")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('file1', css_class='col-md-4'),
                Div('file2', css_class='col-md-4'),
                Div('file3', css_class='col-md-4'),
                css_class='row'),
        )


class OfficeItemForm(forms.ModelForm):
    class Meta:
        model = AppliedItem
        fields = ('item_code', 'spec', 'price', 'qty', 'unit', 'amount', 'received_qty', 'comment')

    item_code = forms.CharField(required=False, label="料號")
    spec = forms.CharField(required=False, label="品名")
    price = forms.IntegerField(required=False, label="參考價格")
    qty = forms.IntegerField(required=False, label="數量")
    unit = forms.CharField(required=False, label="單位")
    amount = forms.IntegerField(required=False, label="參考總價")
    received_qty = forms.IntegerField(required=True, label="已發放數量")
    comment = forms.CharField(required=False, label="備註", widget=forms.Textarea(attrs={'rows': 4, 'cols': 15}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_code'].widget.attrs['readonly'] = True
        self.fields['spec'].widget.attrs['readonly'] = True
        self.fields['price'].widget.attrs['readonly'] = True
        self.fields['qty'].widget.attrs['readonly'] = True
        self.fields['unit'].widget.attrs['readonly'] = True
        self.fields['amount'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('item_code', css_class='col-md-3'),
                Div('spec', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('price', css_class='col-md-3'),
                Div('qty', css_class='col-md-3'),
                Div('unit', css_class='col-md-3'),
                Div('amount', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('received_qty', css_class='col-md-3'),
                css_class='row'),
            Div(
                Div('comment', css_class='col-md-9'),
                css_class='row'),
        )


class ItemSearchForm(forms.Form):
    category = forms.ModelChoiceField(required=False, label="物品類別", queryset=ItemCategory.objects.all(),
                                      to_field_name="catogory_code")
    type = forms.ModelChoiceField(required=False, label="物品種類", queryset=ItemType.objects.none())
    keyword = forms.CharField(required=False, label="關鍵字")
    pic = forms.ChoiceField(label="圖片", choices=(
        ('', '---'), (True, '有'), (False, '無'),), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('category', css_class='col-md-2'),
                Div('type', css_class='col-md-2'),
                Div('pic', css_class='col-md-2'),
                Div('keyword', css_class='col-md-2'),
                Div(Submit('search', '查詢', css_class='btn btn-info'),
                    css_class='col-md-2 d-flex align-items-center search_btn_fix pt-3'),
                css_class='row'),
        )


class ItemModelForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('item_code', 'sap_code', 'vendor_code', 'unit', 'item_type', 'spec', 'price', 'enabled',
                  'item_family', 'item_category', 'is_stock')

    item_code = forms.CharField(required=False, label="料號")
    sap_code = forms.CharField(required=False, label="SAP Code")
    vendor_code = forms.CharField(required=False, label="Vendor Code")
    unit = forms.CharField(required=True, label="單位")
    item_family = forms.ModelChoiceField(required=False, label="大分類", queryset=ItemFamily.objects.all())
    item_category = forms.ModelChoiceField(required=False, label="中分類", queryset=ItemCategory.objects.all())
    item_type = forms.ModelChoiceField(required=True, label="小分類", queryset=ItemType.objects.all())
    spec = forms.CharField(required=True, label="品名")
    price = forms.FloatField(required=False, label="Price", initial=0)
    enabled = forms.ChoiceField(label="啟用", choices=(
            (True, 'True'), (False, 'False'),), required=True)
    is_stock = forms.ChoiceField(label="庫存品", choices=(
            (True, 'True'), (False, 'False'),), required=True, initial=False)


    def __init__(self, *args, submit_title='Submit', **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item_code'].widget.attrs['readonly'] = True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('item_code', css_class='col-md-4'),
                Div('sap_code', css_class='col-md-4'),
                Div('vendor_code', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('item_family', css_class='col-md-4'),
                Div('item_category', css_class='col-md-4'),
                Div('item_type', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('spec', css_class='col-md-12'),
                css_class='row'),
            Div(
                Div('price', css_class='col-md-4'),
                Div('unit', css_class='col-md-4'),
                Div('is_stock', css_class='col-md-4'),
                css_class='row'),
            Div(
                Div('enabled', css_class='col-md-4'),
                css_class='row'),
        )


class TemplateEditForm(forms.Form):
    key_file = forms.FileField(required=False, label="更換鑰匙申請單範本")
    stamp_file = forms.FileField(required=False, label="更換印章申請單範本")
    print_file = forms.FileField(required=False, label="更換印刷品申請單範本")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_errors = True

        self.helper.layout = Layout(
            Div(
                Div('key_file', css_class='col-md-8 pt-3'),
                css_class='row'),
            Div(
                Div('stamp_file', css_class='col-md-8 pt-3'),
                css_class='row'),
            Div(
                Div('print_file', css_class='col-md-8 pt-3'),
                css_class='row'),
        )

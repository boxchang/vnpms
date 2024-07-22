from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from django import forms
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from requests.models import Request
from tests.forms import RTestForm, RTestItemFormSet
from tests.models import Request_test, Request_test_item, Test_result, Test_result_detail


@login_required
def rtest_create(request):
    r = request.GET.get('r')  # 單號id
    try:
        o_request = Request.objects.get(pk=r)
    except Request.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = RTestForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                o_rtest = form.save(commit=False)
                o_rtest.request = o_request
                o_rtest.create_by = request.user
                o_rtest.update_by = request.user
                form.save()

                o_rtest = Request_test.objects.get(pk=o_rtest.id)
                ritem_formset = RTestItemFormSet(
                    request.POST, instance=o_rtest)
                if ritem_formset.is_valid():
                    ritem_formset.save()

            return redirect(o_request.get_absolute_url())
        else:
            errors = form.errors

    form = RTestForm()
    ritem_formset = RTestItemFormSet(
        initial=[{'item': '程式是否符合需求'}, {'item': '程式是否已經push到git'}, ])
    return render(request, 'tests/test_edit.html', locals())


@login_required
def rtest_edit(request):
    r = request.GET.get('r')  # 單號id
    o_request = Request.objects.get(pk=r)
    o_rtest = Request_test.objects.filter(request=o_request).first()

    if request.method == 'POST':
        form = RTestForm(request.POST, instance=o_rtest)
        ritem_formset = RTestItemFormSet(request.POST, instance=o_rtest)
        if form.is_valid() and ritem_formset.is_valid():
            with transaction.atomic():
                o_rtest = form.save(commit=False)
                o_rtest.update_by = request.user
                form.save()
                ritem_formset.save()

        return redirect(o_request.get_absolute_url())
    else:
        form = RTestForm(instance=o_rtest)
        ritem_formset = RTestItemFormSet(instance=o_rtest)
    return render(request, 'tests/test_edit.html', locals())


@login_required
def rtest_delete(request):
    r = request.GET.get('r')  # 單號id
    try:
        o_request = Request.objects.get(pk=r)
    except Request.DoesNotExist:
        raise Http404

    try:
        with transaction.atomic():
            requires = Request_test.objects.filter(request=o_request).all()
            requires.delete()

            results = Test_result.objects.filter(request=o_request).all()
            results.delete()

            o_request.test_data = False
            o_request.save()

    except Exception as e:
        Exception('Unexpected error: {}'.format(e))

    return redirect(o_request.get_absolute_url())


@login_required
def rtest_form(request, pk):
    try:
        o_rtest = Request_test.objects.get(pk=pk)
    except Request_test.DoesNotExist:
        raise Http404

    items = o_rtest.item_test.all()
    choice_list = [(i.pk, i.item) for i in items]

    class BaseTestResultForm(forms.Form):
        item = forms.IntegerField(widget=forms.HiddenInput, required=False)
        item_result = forms.ChoiceField(label=_('result'), choices=(
            (False, 'Failed'), (True, 'Pass'),), required=False)

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = False
            self.helper.layout = Layout(
                Div(Field('item')),
                Div(Field('item_result'), css_class='item_result'),
            )

    class BaseTestResultFormSet(forms.BaseFormSet):
        nonlocal choice_list

        def add_fields(self, form, index):
            super(BaseTestResultFormSet, self).add_fields(form, index)
            form.fields['item_result'].label = choice_list[index][1]

    TestResultFormSet = forms.formset_factory(
        BaseTestResultForm, extra=0, formset=BaseTestResultFormSet)

    if request.method == 'POST':
        formset = TestResultFormSet(request.POST)
        if formset.is_valid():
            with transaction.atomic():
                # 測試結果只要有一筆Failed就是False
                main_result = True
                for f in formset:
                    data = f.cleaned_data
                    if str(data['item_result']).lower() == 'false':
                        main_result = False

                main = Test_result()
                main.request = o_rtest.request
                main.tester = request.user
                main.result = main_result
                main.save()

                for f in formset:
                    data = f.cleaned_data
                    detail = Test_result_detail()
                    detail.item = Request_test_item.objects.get(
                        pk=data['item'])
                    detail.item_result = str(
                        data['item_result']).lower() == 'true'
                    detail.test_result = Test_result.objects.get(pk=main.id)
                    detail.save()

                # 更新測試狀態
                o_rtest.request.test_data = True
                o_rtest.request.save()

            return HttpResponse("<div style='font-size:2em;'>" + str(_(u'You have finished the test data successfully!')) + "</div>")
    else:
        formset = TestResultFormSet(initial=[{'item': i.pk} for i in items])

    return render(request, 'tests/test_form_guest.html', locals())


@login_required
def rtest_result(request, r):
    try:
        o_request = Request.objects.get(pk=r)
    except Request.DoesNotExist:
        raise Http404

    desc = o_request.request_test.first().desc
    o_result = Test_result.objects.filter(request=o_request).all()

    return render(request, 'tests/test_result.html', locals())

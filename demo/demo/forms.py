# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from bootstrap3.tests import TestForm

OWNERS = (
    ('1', 'Shared'),
    ('2', 'Ryan'),
    ('3', 'Jessica'),
)

EXPENSE_CATEGORIS = (
    ('Restaurant', 'Restaurant'),
    ('Grocery', 'Grocery'),
    ('Entertainment', 'Entertainment'),
    ('Electronics', 'Electronics'),
    ('Furniture/Appliances', 'Furniture/Appliances'),
    ('Pets', 'Pets'),
    ('Automobile', (
        ('Gas', 'Gas'),
        ('Insurance', 'Insurance'),
        ('Maintainance', 'Maintainance'),
        ('Repair', 'Repair'),
    )),
    ('Home', (
        ('Rent', 'Rent'),
        ('Water/Waste', 'Water/Waste'),
        ('PG&E', 'PG&E'),
        ('Comcast', 'Comcast'),
    )),
)

class MyTestInput(forms.Form):
    """
    Copied straight out of bootstrap3 TestForm.
    """
    date = forms.DateField(
        required=True,
        label='Expense Date',
        widget=forms.SelectDateWidget,
        initial=datetime.date.today,
    )
    subject = forms.CharField(
        required=True,
        label='Expense Name',
        max_length=100,
        help_text='',
        widget=forms.TextInput(attrs={'placeholder': 'Describe the expense'}),
    )
    amount = forms.DecimalField(
        required=True,
        label='Expense Amount',
        widget=forms.NumberInput(attrs={'placeholder': 'Expense amount in USD'}),
    )
    category = forms.ChoiceField(
        required=True,
        label='Expense Category',
        choices=EXPENSE_CATEGORIS,
    )
    owner = forms.ChoiceField(
        required=True,
        label='Expense Owner',
        choices=OWNERS, widget=forms.RadioSelect
    )

    required_css_class = 'bootstrap3-req'                                                                                                                                                                    

    def clean(self):
       cleaned_data = super(MyTestInput, self).clean()
       raise forms.ValidationError(
            "This error was added to show the non field errors styling."
       )
       return cleaned_data


class ContactForm(MyTestInput):
    pass


class ContactBaseFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super(ContactBaseFormSet, self).add_fields(form, index)

    def clean(self):
        super(ContactBaseFormSet, self).clean()
        raise forms.ValidationError("This error was added to show the non form errors styling")

ContactFormSet = formset_factory(TestForm, formset=ContactBaseFormSet,
                                 extra=2,
                                 max_num=4,
                                 validate_max=True)


class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file5 = forms.ImageField()
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)


class ArticleForm(forms.Form):
    title = forms.CharField()
    pub_date = forms.DateField()

    def clean(self):
        cleaned_data = super(ArticleForm, self).clean()
        raise forms.ValidationError("This error was added to show the non field errors styling.")
        return cleaned_data

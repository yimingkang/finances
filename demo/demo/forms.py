# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory

from bootstrap3.tests import TestForm

OWNERS = (
    ('Shared', 'Shared'),
    ('Ryan', 'Ryan'),
    ('Jessica', 'Jessica'),
)

EXPENSE_CATEGORIS = (
    ('Restaurant', 'Restaurant'),
    ('Grocery', 'Grocery'),
    ('Entertainment', 'Entertainment'),
    ('Electronics', 'Electronics'),
    ('Travel', 'Travel'),
    ('BBT', 'BBT'),
    ('Pets', 'Pets'),
    ('Clothing', 'Clothing'),
    ('Furniture/Appliances', 'Furniture/Appliances'),
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
    ('Others', 'Others'),
)

class UploadExpenseForm(forms.Form):
    owner = forms.ChoiceField(
        required=True,
        label='Expense Owner',
        choices=OWNERS, widget=forms.RadioSelect,
    )
    upload_file = forms.FileField(
        required=True,
        label='Expense File (CSV)',
        widget=forms.ClearableFileInput,
    )

class ExpenseForm(forms.Form):
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
        choices=OWNERS, widget=forms.RadioSelect,
    )

    required_css_class = 'bootstrap3-req'                                                                                                                                                                    

    def clean(self):
       cleaned_data = super(ExpenseForm, self).clean()
       return cleaned_data

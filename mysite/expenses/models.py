from __future__ import unicode_literals

import datetime

from django.db import models

# Create your models here.

class CashFlow(models.Model):
    CURRENCIES = (
        (USD, 'US Dollar'),
        (CAD, 'Canadian Dollar'),
        (RMB, 'Chinese Yuan'),
        (EUR, 'Euro'),
        (GBP, 'Great Britain Pound'),
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
        default=USD,
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    date = models.DateField(
        default=date.today(),
    )

class Expense(CashFlow):
    name = models.CharField(
        max_length=200,
    )
    category = models.CharField(
        max_length=50,
        default='Unknown',
    )
    auto_tax = models.BooleanField(
        default=True,
    )

class NonRecurringExpense(Expense):
    pass

class RecurringExpense(Expense):
    last_expense_date = models.DateField(
        default=date.today(),
    )
    recurring_frequency = models.IntegerField(
        default=14,
    )

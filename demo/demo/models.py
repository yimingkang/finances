from __future__ import unicode_literals

import datetime

from django.db import models

# Create your models here.

class CashFlow(models.Model):
    OWNERS = (
        (1, 'Ryan'),
        (2, 'Jessica'),
        (3, 'Shared'),
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
    )
    date = models.DateField(
        default=datetime.date.today,
    )
    owner = models.CharField(
        max_length=15,
        choices=OWNERS,
    )

class Expense(CashFlow):
    subject = models.CharField(
        max_length=200,
    )
    category = models.CharField(
        max_length=50,
        default='Unknown',
    )

class NonRecurringExpense(Expense):
    pass

class RecurringExpense(Expense):
    last_expense_date = models.DateField(
        default=datetime.date.today,
    )
    recurring_frequency = models.IntegerField(
        default=14,
    )

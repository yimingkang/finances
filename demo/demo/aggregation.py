import datetime
from .models import *

from django.db.models import Sum


class ExpenseAggregator(object):
    COARSE_CATEGORIES = [
            'Restaurant', 'Grocery', 'Entertainment',
            'Electronics', 'Pets', 'Gas', 'Insurance',
            'Rent', 'PG&E', 'Comcast', 'Others',
    ]
    def __init__(self):
        pass

    def aggr_expense_by_category(self):
        #expense_dates = NonRecurringExpense.objects.values('date').annotate(Sum('amount'))
        #dates = [entry['date'] for entry in expense_dates]
        #amounts = [entry['amount__sum'] for entry in expense_dates]
        #return (dates, amounts)
        min_date = datetime.date(2099, 1, 1)
        max_date = datetime.date(2000, 1, 1)
        expense_date_table = dict()
        for entry in NonRecurringExpense.objects.all():
            # manually grab everything
            min_date = min(min_date, entry.date)
            max_date = max(max_date, entry.date)

            if entry.date not in expense_date_table:
                expense_date_table[entry.date] = {k: 0 for k in ExpenseAggregator.COARSE_CATEGORIES}

            if entry.category not in ExpenseAggregator.COARSE_CATEGORIES:
                entry.category = 'Others'
            expense_date_table[entry.date][entry.category] += entry.amount

        # now sort out the dates


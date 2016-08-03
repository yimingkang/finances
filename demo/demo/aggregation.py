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

    def daterange(self, start_date, end_date, recent=None):
        if recent:
            # only generate the most recent k days
            start_date = max(start_date, end_date - datetime.timedelta(recent))
        for n in range(int ((end_date - start_date).days) + 1):
            yield start_date + datetime.timedelta(n)


    def aggr_expense_by_category(self, grain='day', recent=None):
        if grain is 'day':
            return self.aggr_expense_by_category_day(recent)
        else:
            # lets aggregate this motherfucka
            raise ValueError("UNIMPLEMENTED")
            

    def aggr_expense_by_category_day(self, recent=None):
        # recent: only the most recent k days
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

        # now sort out the dates + pull data into a dict
        expense_table = {k: [] for k in ExpenseAggregator.COARSE_CATEGORIES}
        date_table = []
        for date in self.daterange(min_date, max_date, recent):
            date_table.append(str(date))
            if date in expense_date_table:
                # copy over to expense_table
                map(lambda cat: expense_table[cat].append(float(expense_date_table[date][cat])), expense_table.keys())
            else:
                map(lambda cat: expense_table[cat].append(0), expense_table.keys())
        
        # format expense table to a list of dicts that highcharts understands
        return (date_table, [{'name': k, 'data': expense_table[k]} for k in expense_table.keys()])

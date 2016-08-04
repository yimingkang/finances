import datetime
import calendar
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
            start_date = max(start_date, end_date - datetime.timedelta(recent - 1))
        for n in range(int ((end_date - start_date).days) + 1):
            yield start_date + datetime.timedelta(n)

    def aggr_month_to_date(self):
        today = datetime.date.today()
        days_since_1st = int((today - datetime.date(today.year, today.month, 1)).days)

        # here + 1 because "1 day since 1st" ==> "2 most recent days"
        _, expense_table = self.aggr_expense_by_category_day(recent=days_since_1st + 1)
        map(lambda key: expense_table.pop(key), filter(lambda cat: sum(expense_table[cat]) == 0, expense_table.keys()))
        total = reduce(lambda x, y: x + sum(expense_table[y]), expense_table.keys(), 0)
        return ([{'name': cat, 'y': float(sum(expense_table[cat]))} for cat in expense_table.keys()], int(total))

    def aggr_formatter(self, date_table, expense_table):
        # format expense table to a list of dicts that highcharts understands
        return (map(str, date_table), [{'name': k, 'data': expense_table[k]} for k in expense_table.keys()])

    def aggr_expense_by_category(self, grain='day', recent=None):
        dates, expenses = self.aggr_expense_by_category_day(recent)
        if grain is 'day' or len(dates) == 0:
            return self.aggr_formatter(dates, expenses)
        elif grain is 'week':
            start_date = dates[0]
            end_date = dates[-1]

            # figure out the day (monday=0)
            weekday_offset = start_date.weekday()

            # figure out the monday of that week
            start_monday = start_date - datetime.timedelta(weekday_offset)

            # no need to aggregate over days without data
            index = -1 * weekday_offset
            ndays = int((end_date - start_monday).days) + 1

            # new return values!
            new_dates = [start_monday]
            new_expenses = {k: [0]  for k in ExpenseAggregator.COARSE_CATEGORIES}

            for day in xrange(ndays):
                if day % 7 == 0 and index > 0:
                    # push a new monday!
                    new_dates.append(dates[index])
                    map(lambda cat: new_expenses[cat].append(0), ExpenseAggregator.COARSE_CATEGORIES)
                if index >= 0:
                    # now aggregate
                    for cat in ExpenseAggregator.COARSE_CATEGORIES:
                        new_expenses[cat][-1] += expenses[cat][index]
                index += 1
            return self.aggr_formatter(new_dates, new_expenses)
    
        elif grain is 'month':
            # lets aggregate this motherfucka
            raise ValueError("UNIMPLEMENTED")
        elif grain is 'year':
            # lets aggregate this motherfucka
            raise ValueError("UNIMPLEMENTED")
        else:
            # lets aggregate this motherfucka
            raise ValueError("Not a valid granularity: %s" % grain)

    def aggr_expense_by_category_day(self, recent=None):
        # recent: only the most recent k days
        min_date = datetime.date(2099, 1, 1)
        max_date = datetime.date.today()
        expense_date_table = dict()
        for entry in NonRecurringExpense.objects.all():
            # manually grab everything
            min_date = min(min_date, entry.date)

            if entry.date not in expense_date_table:
                expense_date_table[entry.date] = {k: 0 for k in ExpenseAggregator.COARSE_CATEGORIES}

            if entry.category not in ExpenseAggregator.COARSE_CATEGORIES:
                entry.category = 'Others'
            expense_date_table[entry.date][entry.category] += entry.amount

        # now sort out the dates + pull data into a dict
        expense_table = {k: [] for k in ExpenseAggregator.COARSE_CATEGORIES}
        date_table = []
        for date in self.daterange(min_date, max_date, recent):
            date_table.append(date)
            if date in expense_date_table:
                # copy over to expense_table
                map(lambda cat: expense_table[cat].append(float(expense_date_table[date][cat])), expense_table.keys())
            else:
                map(lambda cat: expense_table[cat].append(0), expense_table.keys())
        
        return (date_table, expense_table)

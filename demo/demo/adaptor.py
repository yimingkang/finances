import csv
import datetime
import time
from .models import *

CATEGORY_TRANSLATION = {
    'Clothing/Shoes': 'Clothing',
    'Groceries': 'Grocery',
    'Restaurants/Dining': 'Restaurant',
    'General Merchandise': 'Others',
    'Gasoline/Fuel': 'Gas',
    'Automotive Expenses': 'Maintainance',
    'Entertainment': 'Entertainment',
    'Home Improvement': 'Others',
    'Travel': 'Entertainment',
    'Cable/Satellite Services': 'Comcast',
    'ATM/Cash Withdrawals': 'Others',
    'Electronics': 'Electronics',
    'Hobbies': 'Entertainment',
    'Healthcare/Medical': 'Others',
}


class CSVAdaptor(object):
    def __init__(self, csvfile, owner='Ryan'):
        self.csvfile = csvfile
        self.owner = owner
        self.entries = []
        self.skipped = []
        self.invalid = 0

    def parse_all(self):
        csv_reader = csv.reader(self.csvfile) 
        header = 1
        for row in csv_reader:
            if header:
                header -= 1
                continue
            category = row[4]
            if category not in CATEGORY_TRANSLATION:
                self.skipped.append(",".join([row[2], row[6], row[4]]))
                continue
            subject = row[2]
            amount = float(row[6]) * -1
            date = datetime.date(*time.strptime(row[1], "%m/%d/%Y")[:3])
            try:
                self.entries.append(NonRecurringExpense(
                    owner=self.owner,
                    amount=amount,
                    date=date,
                    subject=subject,
                    category=CATEGORY_TRANSLATION[category],
                    )
                )
            except Exception:
                self.invalid += 1

    def commit(self):
        map(lambda k: k.save(), self.entries)

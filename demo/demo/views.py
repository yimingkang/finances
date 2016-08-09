# -*- coding: utf-8 -*-
from time import localtime, strftime

from django.core.files.storage import default_storage
import json

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from .forms import ExpenseForm 
from .aggregation import *
from .models import *


class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['navbar'] = 'home'

        # render daily view
        date_table, expense_table = ExpenseAggregator().aggr_expense_by_category(grain='day')
        context['data_series'] = expense_table
        context['categories'] = date_table

        # use the # of dates to figure out appropriate tickInterval
        context['ndates'] = len(date_table) 

        # render month to date view
        mtd_data, mtd_total =  ExpenseAggregator().aggr_month_to_date()
        context['mtd_data'] = mtd_data
        context['mtd_total'] = mtd_total
        return context

class CatCamView(TemplateView):
    template_name = 'demo/cat_cam.html'

    def get_context_data(self, **kwargs):
        context = super(CatCamView, self).get_context_data(**kwargs)
        context['navbar'] = 'catcam'

        return context


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    success_url = '/form_horizontal'
    form_class = ExpenseForm 

    def get_context_data(self, **kwargs):
        context = super(FormHorizontalView, self).get_context_data(**kwargs)
        context['navbar'] = 'expense'
        return context

    def form_valid(self, form):
        curdate = strftime("%a %b %d %Y %H:%M:%S", localtime())
        
        #messages.success(self.request, form.data)
        data = form.data
        expense_date = datetime.date(
            int(data['date_year']),
            int(data['date_month']),
            int(data['date_day']),
        )
        try:
            NonRecurringExpense(
                amount=float(data['amount']),
                date=expense_date,
                owner=data['owner'],
                subject=data['subject'],
                category=data['category'],
            ).save()
            messages.success(self.request, "Added a new {cat} expense entry on {time}".format(cat=data['category'], time=curdate))
        except Exception as e:
            messages.error(self.request, "Error entering into database: %s " % e)
            # TODO: handle error
        return super(FormHorizontalView, self).form_valid(form)

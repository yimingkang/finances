# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from time import localtime, strftime

from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

from .forms import ContactForm, FilesForm, ContactFormSet


class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['navbar'] = 'home'
        context['food_expense'] = [50] * 12
        context['entertainment_expense'] = [20] * 12
        return context


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    success_url = '/form_horizontal'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(FormHorizontalView, self).get_context_data(**kwargs)
        context['navbar'] = 'expense'
        return context

    def form_valid(self, form):
        curdate = strftime("%a %b %d %Y %H:%M:%S", localtime())
        messages.success(self.request, "Added a new expense entry on {time}".format(time=curdate))
        return super(FormHorizontalView, self).form_valid(form)

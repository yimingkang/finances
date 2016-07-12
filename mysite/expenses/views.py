import logging

from django.shortcuts import render_to_response
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return render_to_response('test.html')

def render_non_recurring_expense_form(request):
    return HttpResponse("OK")

def render_recurring_expense_form(request):
    return HttpResponse("OK")


# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import patterns, url

from .views import HomePageView, FormHorizontalView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^form_horizontal$', FormHorizontalView.as_view(), name='form_horizontal'),
]

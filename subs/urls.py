#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""""

from django.conf.urls import url

from . import views

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"

urlpatterns = [
      url(r'^$',
          views.home),
      url(r'^calibrate$',
          views.updatevideos),
  ]

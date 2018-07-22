#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""""

import os
from django.core.wsgi import get_wsgi_application

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfg.settings")

application = get_wsgi_application()

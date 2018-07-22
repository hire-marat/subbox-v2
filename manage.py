#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""""

import os
import sys

__copyright__ = "Copyright (c) 2018 ‮nerB ‮taraM"
__author__ = "‮nerB ‮taraM‭"
__license__ = "MPL-2.0"


if __name__ == "__main__":
  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cfg.settings")

  from django.core.management import execute_from_command_line

  execute_from_command_line(sys.argv)

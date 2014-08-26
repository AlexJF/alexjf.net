#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

PLUGINS += ["minify", "optimize_images"]

SITEURL = "http://www.alexjf.net"
RELATIVE_URLS = False

DELETE_OUTPUT_DIRECTORY = True

DISQUS_SITENAME = "alexjf"
GOOGLE_ANALYTICS = "UA-54154002-1"

#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

#######################################################################
#                               GENERAL                               #
#######################################################################

AUTHOR = "Alexandre Fonseca"
SITENAME = "Alex JF"
STARTING_YEAR = 2012
SITEURL = ""
DEBUG = True

THEME = "themes/alexjf"
PLUGIN_PATHS = ["extra/pelican", "extra/pelican-plugins"]
PLUGINS = ["entities", "assets", "autostatic", "advthumbnailer"]

PATH = "content"

TIMEZONE = "Europe/Paris"

DEFAULT_LANG = "en"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

MENU = (("Home", ""),
        ("Blog", "blog"),
        ("About Me", "about-me"),
        ("Projects", "projects"),
        ("Contact", "contact"))

# Blogroll
#LINKS = (("Home", "#"))

# Social widget
SOCIAL = (("Github", "https://github.com/AlexJF"),
          ("Facebook", "https://www.facebook.com/alexandrejorgefonseca"),
          ("Twitter", "https://twitter.com/AlexJFons"),
          ("Google+", "https://plus.google.com/111465526730185768259?rel=author"),
          ("LinkedIn", "http://www.linkedin.com/pub/alexandre-fonseca/18/761/b90"),)

DEFAULT_PAGINATION = 10

#######################################################################
#                             Contents                                #
#######################################################################

PAGE_PATHS = []
ARTICLE_PATHS = []

USE_FOLDER_AS_CATEGORY = False
DEFAULT_DATE = "fs"

DIRECT_TEMPLATES = []
PAGINATED_DIRECT_TEMPLATES = []

ENTITY_TYPES = {
    "Page": {
        "PATHS": ["."],
        "EXCLUDES": ["blog", "projects"],
        "PAGE_URL": "{slug}",
        "PAGE_SAVE_AS": "{slug}/index.html",
        "PATH_METADATA": r"(?P<slug>[^/]+)/.*"
    },
    "Article": {
        "PATHS": ["blog"],
        "ARTICLE_URL": "blog/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/",
        "ARTICLE_SAVE_AS": "blog/{category}/{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html",
        "PATH_METADATA": r".*/(?P<category>[^/]+)/(?P<date>\d{4}/\d{2}/\d{2})/(?P<slug>[^/]+)/.*",
        "DIRECT_TEMPLATES": ["blog"],
        "PAGINATED_DIRECT_TEMPLATES": ["blog"],
        "BLOG_SAVE_AS": "blog/index.html",
        "CATEGORY_TEMPLATE": "category",
        "CATEGORY_URL": 'blog/category/{slug}/',
        "CATEGORY_SAVE_AS": os.path.join('blog', 'category', '{slug}', 'index.html')
    },
    "Project": {
        "PATHS": ["projects"],
        "PROJECT_URL": "projects/{category}/{slug}/",
        "PROJECT_SAVE_AS": "projects/{category}/{slug}/index.html",
        "PATH_METADATA": r".*/(?P<category>[^/]+)/(?P<date>\d{4}/\d{2}/\d{2})/(?P<slug>[^/]+)/.*",
        "DIRECT_TEMPLATES": ["projects"],
        "PAGINATED_DIRECT_TEMPLATES": ["projects"],
        "PROJECTS_SAVE_AS": "projects/index.html",
        "CATEGORY_TEMPLATE": "category",
        "CATEGORY_URL": 'projects/category/{slug}/',
        "CATEGORY_SAVE_AS": os.path.join('projects', 'category', '{slug}', 'index.html')
    }
}

#######################################################################
#                             Extensions                              #
#######################################################################

MD_EXTENSIONS = ["codehilite(css_class=highlight)",
                 "extra",
                 "toc",
                 "linkify",
                 "textalign",
                 "extra.markdown.mdx_collapse"
                ]

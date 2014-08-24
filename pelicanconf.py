#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import collections

import six

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
PLUGINS = ["entities", "assets", "summary", "autostatic", "advthumbnailer", "metadataparsing"]

PATH = "content"

DEFAULT_DATE_FORMAT = "%a, %d %B %Y"
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

STATIC_PATHS = [
    'images/favicon.ico',
    ]

EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'},
    }


Attachment = collections.namedtuple("Attachment", ["url", "name"])
def parse_attachments(string):
    if string is None or not isinstance(string, collections.Iterable):
        return None

    if not isinstance(string, six.string_types):
        string = '\n'.join(string)

    attachments = []

    for line in string.split('\n'):
        if not line:
            continue

        parts = line.split("||")

        url = parts[0].strip()

        if len(parts) == 1:
            name = url
        else:
            name = parts[1].strip()

        attachments.append(Attachment(url, name))

    return attachments


GalleryItem = collections.namedtuple("GalleryItem", ["url", "description"])
def parse_gallery(string):
    if string is None or not isinstance(string, collections.Iterable):
        return None

    if not isinstance(string, six.string_types):
        string = '\n'.join(string)

    items = []

    for line in string.split('\n'):
        if not line:
            continue

        parts = line.split("||")

        url = parts[0].strip()

        if len(parts) == 1:
            description = None
        else:
            description = parts[1].strip()

        items.append(GalleryItem(url, description))

    return items


METADATA_PARSERS = {
    "Attachments": parse_attachments,
    "Gallery": parse_gallery,
}

PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)

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
        "CATEGORY_TEMPLATE": "blog_category",
        "CATEGORY_URL": 'blog/category/{slug}/',
        "CATEGORY_SAVE_AS": os.path.join('blog', 'category', '{slug}', 'index.html')
    },
    "Project": {
        "PATHS": ["projects"],
        "SORT_ATTRIBUTES": "project_start",
        "PROJECT_URL": "projects/{category}/{slug}/",
        "PROJECT_SAVE_AS": "projects/{category}/{slug}/index.html",
        "PATH_METADATA": r".*/(?P<category>[^/]+)/(?P<slug>[^/]+)/.*",
        "DIRECT_TEMPLATES": ["projects"],
        "PAGINATED_DIRECT_TEMPLATES": ["projects"],
        "PROJECTS_SAVE_AS": "projects/index.html",
        "CATEGORY_TEMPLATE": "project_category",
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
                 "textalign",
                 "extra.markdown.mdx_collapse"
                ]

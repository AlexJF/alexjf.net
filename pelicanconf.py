#!/usr/bin/env python
# -*- coding: utf-8 -*- #
import os
import collections
import entities

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
PLUGIN_PATHS = ["extra/pelican-plugins"]
PLUGINS = ["entities", "assets", "summary", "autostatic", "advthumbnailer",
           "metadataparsing"]

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
PATH_METADATA = ""
FILENAME_METADATA = ""

USE_FOLDER_AS_CATEGORY = False
DEFAULT_DATE = "fs"

DIRECT_TEMPLATES = []
PAGINATED_DIRECT_TEMPLATES = []

STATIC_PATHS = [
    'images/favicon.ico',
    'images/favicon.png',
    ]

EXTRA_PATH_METADATA = {
    'images/favicon.ico': {'path': 'favicon.ico'},
    'images/favicon.png': {'path': 'favicon.png'},
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


def parse_description(string):
    if string is None or isinstance(string, six.string_types):
        return string

    if isinstance(string, collections.Iterable):
        string = " ".join(string)

    return string


METADATA_PARSERS = {
    "Attachments": parse_attachments,
    "Gallery": parse_gallery,
    "Description": parse_description,
}

PAGINATION_PATTERNS = (
    (1, '{base_name}/', os.path.join('{base_name}', 'index.html')),
    (2, '{base_name}/page/{number}/', os.path.join('{base_name}', 'page', '{number}', 'index.html')),
)

ENTITY_TYPES = {
    "Page": {
        "PATHS": [""],
        "EXCLUDES": ["blog", "projects"],
        "PAGE_URL": "{slug}",
        "PAGE_SAVE_AS": os.path.join("{slug}", "index.html"),
        "PATH_METADATA": r"(?P<slug>[^/\\]+)(?:/|\\).*",
        "DIRECT_TEMPLATES": ["search"],
        "SEARCH_SAVE_AS": os.path.join("search", "index.html")
    },
    "Article": {
        "PATHS": ["blog"],
        "ARTICLE_URL": "blog/{category}/{slug}/",
        "ARTICLE_SAVE_AS": os.path.join("blog", "{category}", "{slug}", "index.html"),
        "PATH_METADATA": r".*(?:/|\\)(?P<category>[^/\\]+)(?:/|\\)(?P<date>\d{4}-\d{2}-\d{2})(?:/|\\)(?P<slug>[^/\\]+)(?:/|\\).*",
        "DIRECT_TEMPLATES": ["blog"],
        "PAGINATED_DIRECT_TEMPLATES": ["blog"],
        "BLOG_SAVE_AS": os.path.join("blog", "index.html"),
        "CATEGORY_TEMPLATE": "blog_category",
        "CATEGORY_URL": "blog/{slug}/",
        "CATEGORY_SAVE_AS": os.path.join("blog", "{slug}", "index.html"),
        "FEED_ATOM": os.path.join("blog", "feeds", "atom.xml"),
        "CATEGORY_FEED_ATOM": os.path.join("blog", "feeds", "%s.atom.xml")
    },
    "Project": {
        "PATHS": ["projects"],
        "SORTER": entities.attribute_list_sorter(["project_start", "title"], reverse=True),
        "PROJECT_URL": "projects/{category}/{slug}/",
        "PROJECT_SAVE_AS": os.path.join("projects", "{category}", "{slug}", "index.html"),
        "PATH_METADATA": r".*(?:/|\\)(?P<category>[^/\\]+)(?:/|\\)(?P<slug>[^/\\]+)(?:/|\\).*",
        "DIRECT_TEMPLATES": ["projects"],
        "PAGINATED_DIRECT_TEMPLATES": ["projects"],
        "PROJECTS_SAVE_AS": os.path.join("projects", "index.html"),
        "CATEGORY_TEMPLATE": "project_category",
        "CATEGORY_URL": 'projects/{slug}/',
        "CATEGORY_SAVE_AS": os.path.join('projects', '{slug}', 'index.html'),
        "FEED_ATOM": os.path.join("projects", "feeds", "atom.xml"),
        "CATEGORY_FEED_ATOM": os.path.join("projects", "feeds", "%s.atom.xml")
    }
}

#######################################################################
#                             Extensions                              #
#######################################################################

MD_EXTENSIONS = ["codehilite(css_class=highlight)",
                 "extra",
                 "toc",
                 "textalign",
                 "collapse"
                ]

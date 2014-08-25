#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals, print_function

from pelican import signals


def register():
    signals.content_object_init.connect(parse_metadata)


def parse_metadata(instance):
    settings = instance.settings

    custom_metadata_parsers = settings.get("METADATA_PARSERS", None)

    if custom_metadata_parsers:
        for key, parser in custom_metadata_parsers.items():
            key = key.lower()
            if key in instance.metadata:
                instance.metadata[key] = parser(instance.metadata[key])

            if hasattr(instance, key.lower()):
                try:
                    setattr(instance, key.lower(), parser(getattr(instance, key.lower())))
                except AttributeError as e:
                    pass

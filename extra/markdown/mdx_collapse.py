#!/usr/bin/env python
# encoding: utf-8

"""
Collapse Extension for Python-Markdown
======================================

Allow the definition of collapsible blocks in Markdown.

Generated code is designed for compatibility with Bootstrap.

Blocks starting with <<< will start collapsed, blocks
starting with >>> will start uncollapsed.

Syntax:
    <<< [<Panel Id>] "<Panel Title>"
        Paragraph1

        Paragraph2

    or

    >>> [<Panel Id>] "<Panel Title>"
        Paragraph1

        Paragraph2

Based on the Admonition extension.

Example:

    <<< "Collapsible stuff"
        * Stuff 1
        * Stuff 2
        * Stuff 3
        * Stuff 4

    becomes

    <div class="panel panel-default panel-collapsible">
        <div class="panel-heading">
            <a data-toggle="collapse" data-target="#collapse1" />
        </div>
        <div id="collapse1" class="panel-body collapse in">
            <ul>
                <li>Stuff 1</li>
                <li>Stuff 2</li>
                <li>Stuff 3</li>
                <li>Stuff 4</li>
            </ul>
        </div>
    </div>
"""
from __future__ import absolute_import
from __future__ import unicode_literals
import markdown
from markdown.util import etree
import re

class CollapseExtension(markdown.Extension):
    """ Collapse extension for Python-Markdown. """

    def extendMarkdown(self, md, md_globals):
        """ Add Admonition to Markdown instance. """
        md.registerExtension(self)
        md.parser.blockprocessors.add(
            'collapse',
            CollapseProcessor(md.parser), '_begin')

class CollapseProcessor(markdown.blockprocessors.BlockProcessor):
    """ Processor responsible for finding blocks to collapse. """
    BASE_COLLAPSE_ID = 'collapsible-panel-'
    collapse_counter = 0

    WRAPPER_CLASSNAME = 'panel-collapsible'
    WRAPPER_EXTRA_CLASSNAMES = 'panel panel-default'

    HEADING_CLASSNAME = 'panel-heading'
    BODY_CLASSNAME = 'panel-body'

    COLLAPSE_CLASSNAME= 'collapse'
    UNCOLLAPSE_CLASSNAME = 'in'

    COLLAPSE_RE = re.compile(r'(?:^|\n)(<<<|>>>)\ ?([\w\-]+)?(?:\ "(.*?)")')

    def test(self, parent, block):
        sibling = self.lastChild(parent)

        is_collapse_start_block = self.COLLAPSE_RE.search(block)
        is_collapse_continue_block = \
            (block.startswith(' ' * self.tab_length) and sibling and \
             sibling.get('class', '').find(self.WRAPPER_CLASSNAME) != -1)

        return is_collapse_start_block or is_collapse_continue_block

    def run(self, parent, blocks):
        sibling = self.lastChild(parent)
        block = blocks.pop(0)
        collapse_start_block = self.COLLAPSE_RE.search(block)

        if collapse_start_block:
            # removes the first line
            block = block[collapse_start_block.end() + 1:]

        block, rest = self.detab(block)

        if collapse_start_block:
            collapsed, collapse_id, title = self.get_properties(
                collapse_start_block)
            div_wrapper = etree.SubElement(parent, 'div')
            if collapse_id:
                div_wrapper_id = collapse_id
            else:
                div_wrapper_id = self.BASE_COLLAPSE_ID + \
                        str(self.collapse_counter)
            div_wrapper.set('id', div_wrapper_id)
            div_wrapper.set('class', "%s %s" % (self.WRAPPER_CLASSNAME, \
                self.WRAPPER_EXTRA_CLASSNAMES))

            div_heading = etree.SubElement(div_wrapper, 'div')
            div_heading.set('class', self.HEADING_CLASSNAME)
            a_heading = etree.SubElement(div_heading, 'a')
            a_heading.text = title
            a_heading.set('data-toggle', 'collapse')
            a_heading.set('data-target', "#" + div_wrapper_id + " ." + \
                    self.BODY_CLASSNAME)

            div_body = etree.SubElement(div_wrapper, 'div')
            div_body_classnames = self.BODY_CLASSNAME + " " + \
                self.COLLAPSE_CLASSNAME
            if not collapsed:
                div_body_classnames += " " + self.UNCOLLAPSE_CLASSNAME
            div_body.set('class', div_body_classnames)

            self.collapse_counter += 1
        else:
            div_wrapper = sibling
            div_body = self.lastChild(div_wrapper)

        self.parser.parseChunk(div_body, block)

        if rest:
            # This block contained unindented line(s) after the first indented
            # line. Insert these lines as the first block of the master blocks
            # list for future processing.
            blocks.insert(0, rest)

    def get_properties(self, match):
        collapsed = match.group(1) == "<<<"
        collapse_id = match.group(2)
        title = match.group(3)

        return collapsed, collapse_id, title


def makeExtension(*args, **kwargs):
    return CollapseExtension(*args, **kwargs)

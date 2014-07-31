from __future__ import unicode_literals

import re

from markdown.extensions import Extension
from markdown.blockprocessors import BlockProcessor
from markdown.util import etree


class ChecklistProcessor(BlockProcessor):
    # Detect an item (``[X] item``). ``group(1)`` contains contents of item.
    RE = re.compile(r'(^|\n) {0,3}\[([ xX])\] +(.+?)(\n|$)')
    CSS = "checklist"
    # Detect items on secondary lines. they can be of either list type.
    # Detect indented (nested) items of either type

    def test(self, parent, block):
        return bool(self.RE.match(block))

    def run(self, parent, blocks):
        # Check for multiple items in one block.
        items = self.get_items(blocks.pop(0))
        sibling = self.lastChild(parent)

        if sibling is not None and sibling.tag == "ul":
            lst = sibling
        else:
            lst = etree.SubElement(parent, "ul")

        # Loop through items in block, recursively parsing each with the
        # appropriate parent.
        self.parser.state.set('checklist')
        for checked, item in items:
            # New item. Create li and parse with it as parent
            li = etree.SubElement(lst, 'li', **{"class": self.CSS})
            if checked:
                etree.SubElement(li, 'span', **{"class": "glyphicon glyphicon-check"})
            else:
                etree.SubElement(li, 'span', **{"class": "glyphicon glyphicon-unchecked"})
            self.parser.parseBlocks(li, [item])
        self.parser.state.reset()

    def get_items(self, block):
        """ Break a block into list items. """
        items = []
        for line in block.split('\n'):
            m = self.RE.match(line)
            if m:
                # Append to the list
                items.append([m.group(2) in ['x', 'X'], m.group(3)])
            else:
                # This is another line of previous item. Append to that item.
                items[-1][1] = '%s\n%s' % (items[-1][1], line)
        return items


class ChecklistExtension(Extension):

    def extendMarkdown(self, md, md_globals):  # noqa
        md.parser.blockprocessors.add(
            'checklist',
            ChecklistProcessor(md.parser),
            '>ulist',
        )

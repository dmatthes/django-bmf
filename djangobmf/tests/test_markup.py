#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from ..templatetags.djangobmf_markup import markdown_filter


class MarkdownTests(TestCase):
    def test_checklist_empty(self):
        text = "[ ] Test"
        out = markdown_filter(text)
        self.assertEqual(out, '<ul>\n<li class="checklist"><span class="glyphicon glyphicon-unchecked"></span><p>Test</p>\n</li>\n</ul>')

    def test_checklist_checked_x1(self):
        text = "[x] Test"
        out = markdown_filter(text)
        self.assertEqual(out, '<ul>\n<li class="checklist"><span class="glyphicon glyphicon-check"></span><p>Test</p>\n</li>\n</ul>')

    def test_checklist_checked_x2(self):
        text = "[X] Test"
        out = markdown_filter(text)
        self.assertEqual(out, '<ul>\n<li class="checklist"><span class="glyphicon glyphicon-check"></span><p>Test</p>\n</li>\n</ul>')

    def test_checklist_two_lines(self):
        text = '[X] Test\nTest'
        out = markdown_filter(text)
        self.assertEqual(out, '<ul>\n<li class="checklist"><span class="glyphicon glyphicon-check"></span><p>Test\nTest</p>\n</li>\n</ul>')

    def test_checklist_combined1(self):
        text = '[X] Test\n[ ] Test'
        out = markdown_filter(text)
        self.assertEqual(out, '<ul>\n<li class="checklist"><span class="glyphicon glyphicon-check"></span><p>Test</p>\n</li>\n<li class="checklist"><span class="glyphicon glyphicon-unchecked"></span><p>Test</p>\n</li>\n</ul>')

    def test_checklist_combined2(self):
        text = '[X] Test\n\n[ ] Test'
        out = markdown_filter(text)
        self.assertEqual(out, '<ul>\n<li class="checklist"><span class="glyphicon glyphicon-check"></span><p>Test</p>\n</li>\n<li class="checklist"><span class="glyphicon glyphicon-unchecked"></span><p>Test</p>\n</li>\n</ul>')

    def test_strikethrough(self):
        text = "~~deleted~~"
        out = markdown_filter(text)
        self.assertEqual(out, '<p><del>deleted</del></p>')

    def test_urlize_http(self):
        text = "http://example.xo"
        out = markdown_filter(text)
        self.assertEqual(out, '<p><a href="http://example.xo">http://example.xo</a></p>')

    def test_urlize_quoted(self):
        text = "<http://www.example.com>"
        out = markdown_filter(text)
        self.assertEqual(out, '<p><a href="http://www.example.com">http://www.example.com</a></p>')

#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

from __future__ import unicode_literals

from django.test import TestCase

from djangobmf.utils.generate_filename import generate_filename

import re
import os


class GenerateFilenameTests(TestCase):
    def test_file_static(self):
        class Instance(object):
            is_static = True

        filename = generate_filename(Instance(), "file.name")

        self.assertEqual("static/file.name", filename)

    def test_file_static_ct(self):
        class Instance(object):
            is_static = True
            content_id = 0
            class content_type(object):
                name = "contenttype"

        filename = generate_filename(Instance(), "file.name")

        self.assertEqual("static/contenttype/file.name", filename)

    def test_file_static_obj(self):
        class Instance(object):
            is_static = True
            content_id = 1
            class content_type(object):
                name = "contenttype"

        filename = generate_filename(Instance(), "file.name")

        self.assertEqual("static/contenttype/1/file.name", filename)

    def test_file_nonstatic(self):
        def uuidfunction():
            return "aabbcccccc"

        filename = generate_filename(None, "file.name", uuidfunction).split(os.path.sep)

        self.assertEqual(len(filename), 6)
        self.assertTrue(re.match(r'^[0-9]{4}$', filename[0]))
        self.assertTrue(re.match(r'^[0-9]{2}$', filename[1]))
        self.assertEqual("aa", filename[2])
        self.assertEqual("bb", filename[3])
        self.assertEqual("cccccc", filename[4])
        self.assertEqual("file.name", filename[5])

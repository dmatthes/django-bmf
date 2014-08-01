#!/usr/bin/python
# ex:set fileencoding=utf-8:

from flake8.engine import get_style_guide
from unittest import TestCase


class Flake8Test(TestCase):
    def test_flake8(self):
        styleguide = get_style_guide(
            parse_argv=False,
            config_file="tox.ini",
            max_complexity=-1,
            jobs='1',
        )
        styleguide.options.report.start()
        styleguide.input_dir('djangoerp')
        styleguide.options.report.stop()
        count = styleguide.options.report.get_count()
        self.assertEqual(count, 0)

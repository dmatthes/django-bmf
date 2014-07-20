#!/usr/bin/python
# ex:set fileencoding=utf-8:
# flake8: noqa

import os

from flake8.engine import get_style_guide
from pep8 import StandardReport
from unittest import TestCase

class Flake8Test(TestCase):
    def test_flake8(self):

        class Flake8Report(StandardReport):

            def __init__(self, *args, **kwargs):
                super(Flake8Report, self).__init__(*args, **kwargs)
                self._log_messages = []

            def get_file_results(self):
                for line_number, offset, code, text, doc in self._deferred_print:
                    output = self._fmt % {
                        'path': self.filename,
                        'row': self.line_offset + line_number, 'col': offset + 1,
                        'code': code, 'text': text,
                    }
                    self._log_messages.append(output)
                return super(Flake8Report, self).get_file_results()

        StyleGuide = get_style_guide(
            parse_argv=False,
            config_file="tox.ini",
            max_complexity=-1,
            reporter=Flake8Report,
            jobs='1',
        )
        StyleGuide.options.report.start()
        StyleGuide.input_dir('djangoerp')
        StyleGuide.options.report.stop()
        count = StyleGuide.options.report.get_count()
        with open('flakes8.log', 'w') as file:
            for i in sorted(StyleGuide.options.report._log_messages):
                file.write(i+'\n')
        self.assertLess(count, 90)

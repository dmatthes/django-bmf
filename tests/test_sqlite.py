# This is an example test settings file for use with the Django BMF test suite.

from sandbox.test_settings import *

# The 'sqlite3' backend requires only the ENGINE setting (an in-
# memory database will be used). All other backends will require a
# NAME and potentially authentication information. See the
# following section in the docs for more information:
#
# https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3'
    },
}

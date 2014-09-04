
*************
Running tests
*************

There are more ways to do this, here is one way to help you get started::

    # create a virtual environment
    virtualenv test-django-bmf
    # activate it 
    cd test-django-bmf/
    source bin/activate
    # get django BMF from GitHub
    git clone git@github.com:....
    # run the test suite
    python setup.py test

When you run tests against your own new code, don't forget that it's useful to
repeat them for different versions of Python and Django. You can use ``tox`` to
achieve it::

    # get django BMF from GitHub
    git clone git@github.com:glomium/django-bmf.git
    # run the test suite
    tox

Yeah it's that simple!

*************
Writing tests
*************

Write Tests for your Applications
========================================

We usually use the django test-client to do a couple of http-requests to test the view classes,
models and forms you write and modify. You can find examples in the ``djangobmf_contrib`` modules.
This type tests usually cover more than 80% of the application-code. It's a good start.

Write Tests for your the BMF-Core
========================================

At the moment the goal is to increase the test coverage. If you like to help us, look at the coverage Report
and write some tests for modules, which have a poor coverage. Or identify a bug with a testcase :)

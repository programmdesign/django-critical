===============
django-critical
===============

.. image:: https://badge.fury.io/py/django-critical.png
    :target: https://badge.fury.io/py/django-critical

.. image:: https://travis-ci.org/martinblech/django-critical.png?branch=master
    :target: https://travis-ci.org/martinblech/django-critical

.. image:: https://coveralls.io/repos/martinblech/django-critical/badge.png?branch=master
    :target: https://coveralls.io/r/martinblech/django-critical?branch=master

Inlines critical path CSS and defers loading full CSS asynchronously.

Documentation
-------------

The full documentation is at https://django-critical.readthedocs.org.

Quickstart
----------

* Install django-critical:

    .. code-block:: bash

        pip install django-critical

* Add ``critical`` to your ``INSTALLED_APPS`` setting:

    .. code-block:: python

        INSTALLED_APPS = (
            # other apps
            "critical",
        )

* Add ``critical.middleware.CriticalCssMiddleware`` to your
  ``MIDDLEWARE_CLASSES`` setting:

    .. code-block:: python

        MIDDLEWARE_CLASSES = (
            # other middlewares
            "critical.middleware.CriticalCssMiddleware",
        )

* Point your ``CRITICAL_PENTHOUSE_PATH`` setting to the correct path, e.g.:

    .. code-block:: python

        CRITICAL_PENTHOUSE_PATH = os.path.join(
            BASE_DIR, 'node_modules/penthouse/penthouse.js')

* If phantomjs is not in your PATH, you have to set ``CRITICAL_PHANTOMJS_PATH`` and point it to your phantomjs binary:

    .. code-block:: python

        CRITICAL_PHANTOMJS_PATH = os.path.join(
            BASE_DIR, 'node_modules/phantomjs/bin/phantomjs')


How it works
------------

``django-critical`` is activated by adding ``{% load critical %}`` to your template.

``django-critical`` then parses the HTML between ``{% critical %}`` and
``{% endcritical %}`` and searches for CSS.

    .. code-block:: html

        {% critical %}
        <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <style>
          .jumbotron h1 {
            color: red;
          }
        </style>
        {% endcritical %}

It downloads and concatenates all that CSS and uses `penthouse`_ to extract the
critical path CSS rules from it, which end up inlined and minified in place of
the original CSS.

    .. code-block:: html

        <style>html{font-family:sans-serif;-webkit-text-size-adjust:100%…</style>

Later in the HTML, before the closing ``</body>`` tag, the
``{% critical_async %}`` template tag takes care of loading the rest of the CSS
using FilamentGroup's `loadCSS`_.

Caching
-------

``django-critical`` calculates the critical path CSS for the first request,
caches the result and reuses this CSS verbatim for further requests. Most web
applications have different critical path CSS for different groups of pages,
though. This can be solved using the ``{% critical_key "<key>" %}`` template
tag, so that different templates can have different caching keys.

Most likely, you'll have your CSS files in a base template. If you put a key
like e.g., 'base' into your base template, this key will be used, even if
your add another critical key tag to a child template. However, you don't have
to move your CSS to your child templates to render them with differnt keys.
Just load the ``<key>`` dynamically and pass it to your base template.

1. Add critical to your ``base template``

    .. code-block:: html

        {% load critical %}
        {% critical_key key %}
        ...
        <head>
            {% critical %}
            <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
            {% endcritical %}
        </head>
        ...

2. Add a key to the context of your view (e.g,. the view's name)

    .. code-block:: python

        def my_view(request, foo):

            context = {
                'key': 'blog'
            }

You can either set the ``key`` to the same value for several views
(e.g., to all your views rendering your blog), or you can have a distinct
``key`` per page.

    .. note:: The critical key block in your base template overwrites any
        critical keys of your child templates.

Is this stable and ready for production use?
--------------------------------------------

No. ``django-critical`` is in a very early stage of development, so you should
use it at your own risk. `Bug reports`_ and `contributions`_ are welcome,
though!


.. _`penthouse`: https://github.com/pocketjoso/penthouse/
.. _`loadCSS`: https://github.com/filamentgroup/loadCSS
.. _`Bug reports`: https://github.com/martinblech/django-critical/issues
.. _`contributions`: https://github.com/martinblech/django-critical/pulls

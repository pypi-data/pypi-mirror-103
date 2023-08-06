# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pelican', 'pelican.plugins.jinja_filters']

package_data = \
{'': ['*']}

install_requires = \
['pelican>=3,<5', 'titlecase>=1.1.1,<3']

extras_require = \
{'markdown': ['markdown>=3.2,<4.0']}

setup_kwargs = {
    'name': 'pelican-jinja-filters',
    'version': '2.1.0',
    'description': 'Pelican plugin for applying useful Jinja filters in theme templates',
    'long_description': '=============\nJinja Filters\n=============\n\n|build| |pypi|\n\n.. |build| image:: https://img.shields.io/github/workflow/status/pelican-plugins/jinja-filters/build\n    :target: https://github.com/pelican-plugins/jinja-filters/actions\n    :alt: Build Status\n\n.. |pypi| image:: https://img.shields.io/pypi/v/pelican-jinja-filters.svg\n    :target: https://pypi.python.org/pypi/pelican-jinja-filters\n    :alt: PyPI Version\n\n``Jinja Filters`` is a plugin for `Pelican <https://docs.getpelican.com/>`_,\na static site generator written in Python.\n\n``Jinja Filters`` provides a selection of functions (called *filters*) for\ntemplates to use when building your website. They are packaged for Pelican, but\nmay prove useful for other projects that make use of\n`Jinja2 <https://palletsprojects.com/p/jinja/>`_.\n\n\nInstallation\n============\n\nThe easiest way to install ``Jinja Filters`` is through the use of Pip. This\nwill also install the required dependencies (currently ``pelican`` and\n``titlecase``) automatically.\n\n.. code-block:: sh\n\n  pip install pelican-jinja-filters\n\nAs ``Jinja Filters`` is a namespace plugin, assuming you are using Pelican 4.5\n(or newer) **and** *only* other namespace plugins, ``Jinja Filters`` will be\nautomatically be loaded by Pelican. And that\'s it!\n\nIf you are using an older version of Pelican, or non-namespace plugins, you may\nneed to add ``Jinja Filters`` to your ``pelicanconf.py``:\n\n.. code-block:: python\n\n  PLUGINS = [\n      # others...\n      "pelican.plugins.jinja_filters",\n  ]\n\nThe filters are now available for use in your templates.\n\n``Jinja Filters`` supports Pelican from version 4.5 on.\n\n\nUsage\n=====\n\nAt present, the plugin includes the following filters:\n\n- ``datetime`` |--| allows you to change to format displayed for a datetime\n  object. Optionally supply a `datetime format string\n  <https://docs.python.org/3.8/library/datetime.html#strftime-and-strptime-behavior>`_\n  to get a custom format.\n- ``article_date`` |--| a specialized version of ``datetime`` that returns\n  datetimes as wanted for article dates; specifically\n  *Friday, November 4, 2020*.\n- ``breaking_spaces`` |--| replaces non-breaking spaces (HTML code *&nbsp;*)\n  with normal spaces.\n- ``titlecase`` |--| Titlecases the supplied string.\n- ``datetime_from_period`` |--| take the ``period`` provided on period archive\n  pages, and turn it into a proper datetime.datetime object (likely to feed to\n  another filter)\n- ``merge_date_url`` |--| given a datetime (on the left) and a supplied URL,\n  "apply" the date to it. Envisioned in particular for ``YEAR_ARCHIVE_URL``,\n  ``MONTH_ARCHIVE_URL``, and ``DAY_ARCHIVE_URL``.\n\nFor example, within your theme templates, you might have code like:\n\n.. code-block:: html+jinja\n\n    <span class="published">\n        Article Published {{ article.date | article_date }}\n    </span>\n\ngives::\n\n    Article Published Friday, November 4, 2020\n\nOr with your own date format:\n\n.. code-block:: html+jinja\n\n    <span class="published">\n        Article Published {{ article.date | datetime(\'%b %d, %Y\') }}\n    </span>\n\ngives::\n\n    Article Published Nov 04, 2020\n\nFilters can also be chained, or applied in sequence. For example to remove\nbreaking spaces and then titlecase a category name, you might have code like:\n\n.. code-block:: html+jinja\n\n    <a href="{{ SITEURL -}} / {{- article.category.url }}">\n        {{ article.category | breaking_spaces | titlecase }}\n    </a>\n\nOn a Monthly Archive page, you might have the following to link "up" to the\nYearly Archive page:\n\n.. code-block:: html+jinja\n\n    <a href="{{ SITEURL -}} /\n             {{- period | datetime_from_period | merge_date_url(YEAR_ARCHIVE_URL) }}">\n        {{ period | datetime_from_period | datetime(\'%Y\') }}\n    </a>\n\nwhich might give::\n\n    <a href="https://blog.minchin.ca/posts/2017/>2017</a>\n\n\nContributing\n============\n\nContributions are most welcome! See `Contributing`_ for more details.\n\nTo set up a development environment:\n\n1. Fork the project on GitHub, and then clone your fork.\n2. Set up and activate a virtual environment.\n3. Have ``invoke`` on your system path or install it into your virtual\n   environment.\n4. Run ``invoke setup``.\n\nFor more details, see `Contributing`_.\n\n\nLicense\n=======\n\n``Jinja Filters`` is under the MIT License. See attached `License.txt`_ for\nfull license text.\n\n\n.. |--| unicode:: U+2013   .. en dash\n.. _Contributing: https://github.com/pelican-plugins/jinja-filters/blob/master/CONTRIBUTING.md\n.. _License.txt: https://github.com/pelican-plugins/jinja-filters/blob/master/LICENSE.txt\n',
    'author': 'William Minchin',
    'author_email': 'w_minchin@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pelican-plugins/jinja-filters',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)

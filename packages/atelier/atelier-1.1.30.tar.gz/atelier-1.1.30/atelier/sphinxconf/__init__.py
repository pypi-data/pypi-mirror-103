# -*- coding: utf-8 -*-
# Copyright 2011-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

"""
Sphinx extensions and a :func:`configure` function used to build
the documentation trees maintained by us.


.. toctree::

.. autosummary::
   :toctree:

   base
   dirtables
   refstothis
   insert_input
   sigal_image
   complex_tables
   blog
   interproject
"""

import logging ; logger = logging.getLogger(__name__)

import sys

from pathlib import Path
from pkg_resources import parse_version
import sphinx
import atelier
from atelier.projects import get_project_from_path

def configure(globals_dict):
    """
    Adds to your `conf.py` an arbitrary series of things that all my
    Sphinx docs configuration files have in common.

    To be called from inside the Sphinx `conf.py` as follows::

      from atelier.sphinxconf import configure
      configure(globals())

    Incomplete list of `conf.py` settings that will be set:

    - `templates_path`
    - `extensions`, `extlinks` and `intersphinx_mapping` are initialized but empty
    - `master_doc` = 'index'
    - `source_suffix` = '.rst'
    - `primary_domain` = 'py'
    - `pygments_style` = 'sphinx'
    - `version` and `release` from SETUP_INFO
    - `exclude_trees` = ['old', 'include', '.build']

    """
    docs_root = Path(globals_dict['__file__']).parent.absolute()
    sys.path.append(docs_root)
    atelier.current_project = get_project_from_path(docs_root.parent)
    atelier.current_project.load_info()

    globals_dict.setdefault('html_context', dict()).update(
        SETUP_INFO=atelier.current_project.SETUP_INFO)

    version = atelier.current_project.SETUP_INFO.get('version', None)
    if version:
        globals_dict.update(release=version)
        globals_dict.update(version='.'.join(version.split('.')[:2]))

    globals_dict.setdefault('extlinks', dict())
    globals_dict.setdefault('intersphinx_mapping', dict())
    globals_dict.update(exclude_patterns=['old', 'include', 'shared', '.build'])
    globals_dict.update(extensions=[
        'sphinx.ext.autodoc',
        'sphinx.ext.autosummary',
        'sphinx.ext.inheritance_diagram',
        'sphinx.ext.todo',
        'sphinx.ext.extlinks',
        'sphinx.ext.graphviz',
        'sphinx.ext.intersphinx',
        # no i18n, no discovery, only one entry per doc,
        # 'sphinxcontrib.newsfeed',
        #~ 'sphinx.ext.doctest',
        'atelier.sphinxconf.base',
        'atelier.sphinxconf.dirtables',
        'atelier.sphinxconf.refstothis',
        'atelier.sphinxconf.insert_input',
    ])

    # default config for autosummary:
    globals_dict.update(autosummary_generate=True)
    if parse_version(sphinx.__version__) < parse_version("1.8"):
        globals_dict.update(autodoc_default_flags=[
            'show-inheritance', 'members'])

    else:
        globals_dict.update(autodoc_default_options={
            'members': None, 'show-inheritance': None})

    mydir = Path(__file__).parent.absolute()
    tp = globals_dict.setdefault('templates_path', [])
    tp += ['.templates', str(mydir)]

    # globals_dict.update(html_static_path=['.static'])

    # Some settings I use in all projects:

    globals_dict.update(master_doc='index')
    globals_dict.update(source_suffix='.rst')
    globals_dict.update(primary_domain='py')
    globals_dict.update(pygments_style='sphinx')

    globals_dict.update(autodoc_member_order='bysource')
    globals_dict.update(autodoc_inherit_docstrings=False)

    if True:
        # globals_dict.update(html_theme="bizstyle")
        globals_dict.update(html_theme="sphinx_rtd_theme")
        globals_dict.update(html_theme_options={
            "prev_next_buttons_location": "both",
            "style_nav_header_background": "#dddddd",
            "style_external_links": False,  # disadvantage: line spacing increases for lines with a link
            "includehidden": False,
        })
    else:
        # use default html_theme ("alabaster")
        globals_dict.update(html_theme="alabaster")
        my_font_family = "Swiss, Helvetica, 'Liberation Sans'"
        globals_dict.update(html_theme_options={
            "font_family": my_font_family,
            "head_font_family": my_font_family,
        })


    # globals_dict.update(
    #     blogref_format="http://www.lino-framework.org/blog/%Y/%m%d.html")


def version2rst(self, m):
    """
    used in docs/released/index.rst
    """
    v = m.__version__
    if v.endswith('+'):
        v = v[:-1]
        print("The current stable release is :doc:`%s`." % v)
        print("We are working on a future version in the code repository.")
    elif v.endswith('pre'):
        print("We're currently working on :doc:`%s`." % v[:-3])
    else:
        print("The current stable release is :doc:`%s`." % v)
        #~ print("We're currently working on :doc:`coming`.")

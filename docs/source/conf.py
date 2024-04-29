import os
import sys
import time
import re
import pkgutil
import string
import f5_sphinx_theme
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# REQUIRED: Your class/lab name
classname = "F5 Distributed Cloud"

sys.path.insert(0, os.path.abspath("."))

year = time.strftime("%Y")

project = 'BIG-IP to XC'
copyright = '2024, Michael Coleman'
author = 'Michael Coleman'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.extlinks",
    "sphinx.ext.graphviz",
    "sphinxcontrib.nwdiag",
    "sphinx_copybutton",
    "sphinxcontrib.blockdiag"
    # "sphinx.ext.autosectionlabel"
]

graphviz_output_format = "svg"
graphviz_font = "DejaVu Sans:style=Book"
graphviz_dot_args = [
    "-Gfontname='%s'" % graphviz_font,
    "-Nfontname='%s'" % graphviz_font,
    "-Efontname='%s'" % graphviz_font,
]

diag_fontpath = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
diag_html_image_format = "SVG"
diag_latex_image_format = "PNG"
diag_antialias = False

blockdiag_fontpath = nwdiag_fontpath = diag_fontpath
blockdiag_html_image_format = nwdiag_html_image_format = diag_html_image_format
blockdiag_latex_image_format = nwdiag_latex_image_format = diag_latex_image_format
blockdiag_antialias = nwdiag_antialias = diag_antialias

eggs_loader = pkgutil.find_loader("sphinxcontrib.spelling")
found = eggs_loader is not None

if found:
    extensions += ["sphinxcontrib.spelling"]
    spelling_lang = "en_US"
    spelling_word_list_filename = "../wordlist"
    spelling_show_suggestions = True
    spelling_ignore_pypi_package_names = False
    spelling_ignore_wiki_words = True
    spelling_ignore_acronyms = True
    spelling_ignore_python_builtins = True
    spelling_ignore_importable_modules = True
    spelling_filters = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html4_writer = True
html_theme = "f5_sphinx_theme"
html_theme_path = f5_sphinx_theme.get_html_theme_path()
html_sidebars = {"**": ["searchbox.html", "localtoc.html", "globaltoc.html"]}
html_theme_options = {
    "site_name": "Community Training Classes & Labs",
    "next_prev_link": True
}
html_codeblock_linenos_style = 'table'
#html_context = {"github_url": github_repo}

html_last_updated_fmt = "%Y-%m-%d %H:%M:%S"

#extlinks = {"issues": (("%s/issues/%%s" % github_repo), "issue ")}
html_static_path = ['_static']

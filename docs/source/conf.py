import f5_sphinx_theme
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'BIG-IP to XC'
copyright = '2024, Michael Coleman'
author = 'Michael Coleman'
release = '2024'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []

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

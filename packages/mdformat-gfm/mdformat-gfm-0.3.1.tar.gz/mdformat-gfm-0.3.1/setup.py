# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mdformat_gfm']

package_data = \
{'': ['*']}

install_requires = \
['linkify-it-py>=1.0.0,<2.0.0',
 'markdown-it-py>=1.0.0b2,<2.0.0',
 'mdformat-tables>=0.4.0',
 'mdformat>=0.7.5,<0.8.0',
 'mdit-py-plugins>=0.2.0,<0.3.0']

entry_points = \
{'mdformat.parser_extension': ['gfm = mdformat_gfm.plugin']}

setup_kwargs = {
    'name': 'mdformat-gfm',
    'version': '0.3.1',
    'description': 'Mdformat plugin for GitHub Flavored Markdown compatibility',
    'long_description': '[![Build Status](https://github.com/hukkinj1/mdformat-gfm/workflows/Tests/badge.svg?branch=master)](https://github.com/hukkinj1/mdformat-gfm/actions?query=workflow%3ATests+branch%3Amaster+event%3Apush)\n[![PyPI version](https://img.shields.io/pypi/v/mdformat-gfm)](https://pypi.org/project/mdformat-gfm)\n\n# mdformat-gfm\n\n> Mdformat plugin for GitHub Flavored Markdown compatibility\n\n## Description\n\n[Mdformat](https://github.com/executablebooks/mdformat) is a formatter for\n[CommonMark](https://spec.commonmark.org/current/)\ncompliant Markdown.\n\nMdformat-gfm is an mdformat plugin that changes the target specification to\n[GitHub Flavored Markdown (GFM)](https://github.github.com/gfm/),\nmaking the tool able to format the following syntax extensions:\n\n- [tables](https://github.github.com/gfm/#tables-extension-)\n- [task list items](https://github.github.com/gfm/#task-list-items-extension-)\n- [strikethroughs](https://github.github.com/gfm/#strikethrough-extension-)\n- [autolinks](https://github.github.com/gfm/#autolinks-extension-)\n- [disallowed raw HTML](https://github.github.com/gfm/#disallowed-raw-html-extension-)\n  (note that no changes are required from a formatter to support this extension)\n\n## Install\n\n```sh\npip install mdformat-gfm\n```\n\n## Usage\n\n```sh\nmdformat <filename>\n```\n',
    'author': 'Taneli Hukkinen',
    'author_email': 'hukkinj1@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/hukkinj1/mdformat-gfm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)

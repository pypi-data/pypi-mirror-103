# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['nginxfmt']
entry_points = \
{'console_scripts': ['nginxfmt = nginxfmt:main']}

setup_kwargs = {
    'name': 'nginxfmt',
    'version': '1.2.2',
    'description': 'nginx config file formatter/beautifier with no additional dependencies.',
    'long_description': '# *nginx* config file formatter/beautifier\n\n*nginx* config file formatter/beautifier written in Python with no additional dependencies. It can be used as library or standalone script. It formats *nginx* configuration files in consistent way, described below:\n\n* All lines are indented in uniform manner, with 4 spaces per level. Number of spaces is customizable.\n* Neighbouring empty lines are collapsed to at most two empty lines.\n* Curly braces placement follows Java convention.\n* Whitespaces are collapsed, except in comments and quotation marks.\n\n\n## Installation\n\nPython 3.4 or later is needed to run this program. The easiest way is to download package from PyPI:\n\n```bash\npip3 install nginxfmt\n```\n\n\n### Manual installation\n\nThe simplest form of installation would be copying `nginxfmt.py` to\nyour scripts directory. It has no 3-rd party dependencies.\n\nYou can also clone the repository and symlink the executable:\n\n```\ncd\ngit clone https://github.com/slomkowski/nginx-config-formatter.git\nln -s ~/nginx-config-formatter/nginxfmt.py ~/bin/nginxfmt.py\n```\n\n\n## Usage as standalone script\n\nIt can format one or several files. Result is by default saved to the original file, but can be redirected to *stdout*.\nIt can also function in piping mode, with `--pipe` switch.\n\n```\nusage: nginxfmt.py [-h] [-v] [-] [-p | -b] [-i INDENT] [config_files ...]\n\nFormats nginx configuration files in consistent way.\n\npositional arguments:\n  config_files          configuration files to format\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -v, --verbose         show formatted file names\n  -, --pipe             reads content from standard input, prints result to stdout\n  -p, --print-result    prints result to stdout, original file is not changed\n  -b, --backup-original\n                        backup original config file as filename.conf~\n\nformatting options:\n  -i INDENT, --indent INDENT\n                        specify number of spaces for indentation\n```\n\n\n## Using as library\n\nMain logic is within `Formatter` class, which can be used in 3rd-party code.\n\n```python\nimport nginxfmt\n\n# initializing with standard FormatterOptions\nf = nginxfmt.Formatter()\n\n# format from string\nformatted_text = f.format_string(unformatted_text)\n\n# format file and save result to the same file\nf.format_file(unformatted_file_path)\n\n# format file and save result to the same file, original unformatted content is backed up\nf.format_file(unformatted_file_path, backup_path)\n```\n\nCustomizing formatting options:\n\n```python\nimport nginxfmt\n\nfo = nginxfmt.FormatterOptions()\nfo.indentation = 2  # 2 spaces instead of default 4\n\n# initializing with standard FormatterOptions\nf = nginxfmt.Formatter(fo)\n```\n\n\n## Reporting bugs\n\nPlease create issue under https://github.com/slomkowski/nginx-config-formatter/issues. Be sure to add config snippets to\nreproduce the issue, preferably:\n\n* snippet do be formatted\n* actual result with invalid formatting\n* desired result\n\n\n## Credits\n\nCopyright 2021 Michał Słomkowski. License: Apache 2.0. Previously published under https://github.com/1connect/nginx-config-formatter.\n',
    'author': 'Michał Słomkowski',
    'author_email': 'michal@slomkowski.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/slomkowski/nginx-config-formatter',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.4',
}


setup(**setup_kwargs)

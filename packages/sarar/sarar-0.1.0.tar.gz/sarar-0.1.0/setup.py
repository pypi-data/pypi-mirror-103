# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sarar', 'sarar.commands']

package_data = \
{'': ['*']}

install_requires = \
['asteval>=0.9.23,<0.10.0',
 'click>=7.1.2,<8.0.0',
 'pycron>=3.0.0,<4.0.0',
 'ruamel.yaml>=0.16.13,<0.17.0',
 'typeguard>=2.12.0,<3.0.0']

entry_points = \
{'console_scripts': ['sarar = sarar.sarar:main']}

setup_kwargs = {
    'name': 'sarar',
    'version': '0.1.0',
    'description': 'SARAR is a command-line-interface tool for GNU/Linux, its goal is to optimize the process of remembering things.',
    'long_description': '![Build status](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_build.svg)\n![Documentation status](https://readthedocs.org/projects/sarar/badge/?version=latest)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n![Coverage](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_coverage.svg)\n![Pylint score](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_pylint.svg)\n<!--![Repo Size](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_size.svg) -->\n![License](https://img.shields.io/badge/license-GPLv3-success)\n\n# SARAR - Spaced And Repeated Active Recaller\n\nSARAR is a command-line-interface tool for GNU/Linux, its goal is to optimize the process of\nremembering things. It is somewhat similar to [Anki](https://docs.ankiweb.net/#/background) and\n[SuperMemo](https://www.supermemo.com/en), i.e. it is a [flashcard\nprogram](https://en.wikipedia.org/wiki/Flashcard) that is based on two key concepts:\n\n1. [Active recall](https://en.wikipedia.org/wiki/Active_recall): a learning technique, usually\n   based on answering questions/flashcards ("active" memory stimulation). In contrast to passive\n   techniques, in which the learning material is processed e.g. by reading, watching, etc.\n\n2. [Spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition): another learning\n   technique, in which newly introduced and more difficult learning material is shown more\n   frequently, while older and less difficult is shown less frequently. In contrast to massed\n   practice, in which learning material is learned "at once".\n\nThe main difference between this project and [alternative flashcard\nprograms](https://en.wikipedia.org/wiki/Spaced_repetition#List_of_spaced_repetition_software_programs)\nis that SARAR focuses on keeping things dead simple, minimal and usable, with more advanced and\nexperienced GNU/Linux users in mind: see the [suckless\nphilosphy](https://suckless.org/philosophy/).\n\n> Note that SARAR is unfortunately *not* suckless, because - among other things - of its\n> dependencies, its total number of lines of code and also probably its [non-trivial development\n> process](https://sarar.readthedocs.io/en/latest/developer-guide/get-started-and-contribute/), but\n> still: the [suckless philosphy](https://suckless.org/philosophy/) is a reference that guides the\n> project.\n\n---\n## Table of contents\n\n<!-- vim-markdown-toc GitLab -->\n\n* [Core scientific guidelines](#core-scientific-guidelines)\n* [Disclamer](#disclamer)\n* [Change log](#change-log)\n* [Status](#status)\n* [User guide](#user-guide)\n* [Developer guide](#developer-guide)\n* [License](#license)\n\n<!-- vim-markdown-toc -->\n\n---\n## Core scientific guidelines\n\nSee [the key scientific assumptions that are guiding the development of\nSARAR](https://sarar.readthedocs.io/en/latest/scientific-guidelines/).\n\n---\n## Disclamer\n\n**SARAR is not pretending to be a "superior" alternative to\n[Anki](https://docs.ankiweb.net/#/background) or [any other flashcard\nprogram](https://en.wikipedia.org/wiki/Spaced_repetition#List_of_spaced_repetition_software_programs)!**\n\nSARAR is just intended for users who prefer command line interfaces, primarily seeking minimalism\nand simplicity.\n\n---\n## Change log\n\nSee [the change log](https://sarar.readthedocs.io/en/latest/CHANGELOG/).\n\n---\n## Status\n\nSARAR is in its early stages of development, it is not yet functional, please give it some time to\ngrow and come back to see how it evolves in a little while.\n\n---\n## User guide\n\n* [Install - Uninstall -\n  Update](https://sarar.readthedocs.io/en/latest/user-guide/install-uninstall-update/)\n* [Basic usage](https://sarar.readthedocs.io/en/latest/user-guide/basic-usage/)\n* [SARARA - SARAR\n  Architecture](https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture/)\n* [Configuration](https://sarar.readthedocs.io/en/latest/user-guide/configuration/)\n* [Commands](https://sarar.readthedocs.io/en/latest/user-guide/commands/check-deck/)\n\n---\n## Developer guide\n\n* [Project layout](https://sarar.readthedocs.io/en/latest/developer-guide/project-layout/)\n* [Get started and\n  contribute](https://sarar.readthedocs.io/en/latest/developer-guide/get-started-and-contribute/)\n\n---\n## License\n\nThe [license used for this project](https://sarar.readthedocs.io/en/latest/LICENSE/) is the [GNU\nGPLv3 license](https://en.wikipedia.org/wiki/GNU_General_Public_License#Version_3).\n',
    'author': 'Stéphane Tzvetkov',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

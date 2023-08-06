![Build status](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_build.svg)
![Documentation status](https://readthedocs.org/projects/sarar/badge/?version=latest)
![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)
![Coverage](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_coverage.svg)
![Pylint score](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_pylint.svg)
<!--![Repo Size](https://gitlab.com/stephane.tzvetkov/sarar/-/raw/master/.badge_size.svg) -->
![License](https://img.shields.io/badge/license-GPLv3-success)

# SARAR - Spaced And Repeated Active Recaller

SARAR is a command-line-interface tool for GNU/Linux, its goal is to optimize the process of
remembering things. It is somewhat similar to [Anki](https://docs.ankiweb.net/#/background) and
[SuperMemo](https://www.supermemo.com/en), i.e. it is a [flashcard
program](https://en.wikipedia.org/wiki/Flashcard) that is based on two key concepts:

1. [Active recall](https://en.wikipedia.org/wiki/Active_recall): a learning technique, usually
   based on answering questions/flashcards ("active" memory stimulation). In contrast to passive
   techniques, in which the learning material is processed e.g. by reading, watching, etc.

2. [Spaced repetition](https://en.wikipedia.org/wiki/Spaced_repetition): another learning
   technique, in which newly introduced and more difficult learning material is shown more
   frequently, while older and less difficult is shown less frequently. In contrast to massed
   practice, in which learning material is learned "at once".

The main difference between this project and [alternative flashcard
programs](https://en.wikipedia.org/wiki/Spaced_repetition#List_of_spaced_repetition_software_programs)
is that SARAR focuses on keeping things dead simple, minimal and usable, with more advanced and
experienced GNU/Linux users in mind: see the [suckless
philosphy](https://suckless.org/philosophy/).

> Note that SARAR is unfortunately *not* suckless, because - among other things - of its
> dependencies, its total number of lines of code and also probably its [non-trivial development
> process](https://sarar.readthedocs.io/en/latest/developer-guide/get-started-and-contribute/), but
> still: the [suckless philosphy](https://suckless.org/philosophy/) is a reference that guides the
> project.

---
## Table of contents

<!-- vim-markdown-toc GitLab -->

* [Core scientific guidelines](#core-scientific-guidelines)
* [Disclamer](#disclamer)
* [Change log](#change-log)
* [Status](#status)
* [User guide](#user-guide)
* [Developer guide](#developer-guide)
* [License](#license)

<!-- vim-markdown-toc -->

---
## Core scientific guidelines

See [the key scientific assumptions that are guiding the development of
SARAR](https://sarar.readthedocs.io/en/latest/scientific-guidelines/).

---
## Disclamer

**SARAR is not pretending to be a "superior" alternative to
[Anki](https://docs.ankiweb.net/#/background) or [any other flashcard
program](https://en.wikipedia.org/wiki/Spaced_repetition#List_of_spaced_repetition_software_programs)!**

SARAR is just intended for users who prefer command line interfaces, primarily seeking minimalism
and simplicity.

---
## Change log

See [the change log](https://sarar.readthedocs.io/en/latest/CHANGELOG/).

---
## Status

SARAR is in its early stages of development, it is not yet functional, please give it some time to
grow and come back to see how it evolves in a little while.

---
## User guide

* [Install - Uninstall -
  Update](https://sarar.readthedocs.io/en/latest/user-guide/install-uninstall-update/)
* [Basic usage](https://sarar.readthedocs.io/en/latest/user-guide/basic-usage/)
* [SARARA - SARAR
  Architecture](https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture/)
* [Configuration](https://sarar.readthedocs.io/en/latest/user-guide/configuration/)
* [Commands](https://sarar.readthedocs.io/en/latest/user-guide/commands/check-deck/)

---
## Developer guide

* [Project layout](https://sarar.readthedocs.io/en/latest/developer-guide/project-layout/)
* [Get started and
  contribute](https://sarar.readthedocs.io/en/latest/developer-guide/get-started-and-contribute/)

---
## License

The [license used for this project](https://sarar.readthedocs.io/en/latest/LICENSE/) is the [GNU
GPLv3 license](https://en.wikipedia.org/wiki/GNU_General_Public_License#Version_3).

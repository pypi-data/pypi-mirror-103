"""
SARAR
"""

# NOTE: write to .deck: https://kutt.it/nUqGbC

import os

import atexit
from pathlib import Path

import click
from sarar.click_utils import MutuallyExclusiveOption, Map

import sarar.commands.check_deck as cd
import sarar.commands.print_deck as pd

__version__ = "0.1.0"

HELP_PATH = Path(os.path.realpath(__file__)).parent.parent / "docs" / "user-guide" / "commands"
CONTEXT_SETTINGS = dict(
    obj={
        "collection": os.path.join(Path.home(), ".local/share/SARAR/collection/"),
        # 'conf': os.path.join(Path.home(), '.config/SARAR/SARAR.conf'),
    },
)


def doc_to_help(doc_file_md):
    """
    Converts a command's documentation into a command's help message.
    """
    help_page = str(
        Path(doc_file_md)
        .read_text()
        .replace("!!!tip ", "")
        .replace("!!!+tip ", "")
        .replace("!!! tip ", "")
        .replace("!!!abstract ", "")
        .replace("!!!+abstract ", "")
        .replace("!!! abstract ", "")
        .replace("\n", "\n\t")
        # .replace("SYNOPSIS", "\b\b\b\b\b\b\b\bSYNOPSIS")
        # .replace("OVERVIEW", "\b\b\b\b\b\b\b\bOVERVIEW")
        # .replace("DESCRIPTION", "\b\b\b\b\b\b\b\bDESCRIPTION")
        # .replace("OPTIONS", "\b\b\b\b\b\b\b\bOPTIONS")
        # .replace("EXAMPLES", "\b\b\b\b\b\b\b\bEXAMPLES")
        # .replace("DETAILS", "\b\b\b\b\b\b\b\bDETAILS")
        # .replace("NOTES", "\b\b\b\b\b\b\b\bNOTES")
        # .replace("LICENSE", "\b\b\b\b\b\b\b\bLICENSE")
        .replace("#!Bash ", "")
        .replace("#!MySQL ", "")
        .replace("<br />", "")
        .replace("<br/>", "")
        .replace("#### ", "\b\b\b\b\b\b\b\b")
        .replace("### ", "\b\b\b\b\b\b\b\b")
        .replace("## ", "\b\b\b\b\b\b\b\b")
        .replace("# ", "\b\b\b\b\b\b\b\b")
    )
    return help_page


@atexit.register
def cleanup():
    """
    Runs after every other Click commands, this is the last function to be executed (cleanup).
    """
    map_ctx = Map(CONTEXT_SETTINGS)
    if "debug" in map_ctx.obj:
        debug = map_ctx.obj["debug"]
        click.echo(f"\n`{debug}`.\n")

    # if "collection" in map_ctx.obj:
    #     collection = map_ctx.obj['collection']
    #     click.echo(f"\n`{collection}`.\n")

    # if "conf" in map_ctx.obj:
    #     conf = map_ctx.obj['conf']
    #     click.echo(f"\n`{conf}`.\n")


@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    "-c", "--collection", "collection", type=click.Path(), help="Path to SARAR's decks collection."
)
@click.option(
    "-v",
    "--version",
    "version",
    is_flag=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["collection"],
)
@click.version_option(version=__version__, message="SARAR version %(version)s")
@click.pass_context
def main(ctx, collection, version):  # pylint: disable=unused-argument
    """
    SARAR is a command-line-interface tool for GNU/Linux, its goal is to optimize the process of
    remembering things.

    It is somewhat similar to Anki (see https://docs.ankiweb.net/#/background) and
    SuperMemo (see https://www.supermemo.com/en), i.e. it is a flashcard
    program (see https://en.wikipedia.org/wiki/Flashcard) that is based on two key concepts:

    1. Active recall (see https://en.wikipedia.org/wiki/Active_recall): a learning technique,
    usually based on answering questions/flashcards ("active" memory stimulation). In contrast to
    passive techniques, in which the learning material is processed e.g. by reading, watching, etc.

    2. Spaced repetition (see https://en.wikipedia.org/wiki/Spaced_repetition): another learning
    technique, in which newly introduced and more difficult learning material is shown more
    frequently, while older and less difficult is shown less frequently. In contrast to massed
    practice, in which learning material is learned "at once".

    The main difference between this project and alternative flashcard programs (see
    https://en.wikipedia.org/wiki/Spaced_repetition#List_of_spaced_repetition_software_programs) is
    that SARAR focuses on keeping things dead simple, minimal and usable, with more advanced and
    experienced GNU/Linux users in mind: see the suckless
    philosphy (https://suckless.org/philosophy/) (note that SARAR is unfortunately *not* suckless,
    because - among other things - of its dependencies and its number of lines of code, but **SARAR
    aims to be as much suckless as possible**).

    \f
    Main function / entry point of SARAR.
    """
    if collection:
        ctx.obj["collection"] = collection


@main.command()
@click.option(
    "-d",
    "--deck-path",
    "deck_path",
    type=click.Path(),
    help="Path to the deck to be checked.",
    # required=True,
)
@click.option(
    "-h",
    "--help",
    "hlp",
    is_flag=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["deck_path"],
)
@click.pass_context
def check_deck(ctx, deck_path, hlp):  # pylint: disable=unused-argument
    """
    \f
    check-deck command

    For more details:
    * see docs/user-guide/commands/check-deck.md
    * see sarar/check-deck.py
    """

    if deck_path:
        cd.check_deck(deck_path)
    else:
        # if no option is passed, or if the -h --help option is passed, then print associated doc:
        check_deck_doc_path = HELP_PATH / "check-deck.md"
        click.echo(doc_to_help(check_deck_doc_path))


@main.command()
@click.option(
    "-d",
    "--deck-path",
    "deck_path",
    type=click.Path(),
    help="Path to the deck to print.",
    # required=True,
)
@click.option(
    "-h",
    "--help",
    "hlp",
    is_flag=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["deck_path"],
)
@click.pass_context
def print_deck(ctx, deck_path, hlp):  # pylint: disable=unused-argument
    """
    \f
    print-deck command

    For more details:
    * see docs/user-guide/commands/print-deck.md
    * see sarar/print-deck.py
    """

    if deck_path:
        pd.print_deck(deck_path)
    else:
        # if no option is passed, or if the -h --help option is passed, then print associated doc:
        print_deck_doc_path = HELP_PATH / "print-deck.md"
        click.echo(doc_to_help(print_deck_doc_path))


# @main.command()
# # @click.option('--n', default=1, show_default=True, required=True, type=int)
# # @click.option('--password', prompt="Password:", hide_input=True, confirmation_prompt=True)
# @click.option('-b', '--blah')
# @click.option('-p', '--plop', cls=MutuallyExclusiveOption, mutually_exclusive=["test", "blah"])
# # @click.option('-t', '--test', cls=MutuallyExclusiveOption, mutually_exclusive=["plop"])
# @click.option('-t', '--test', cls=MutuallyExclusiveOption)
# @click.pass_context
# def test(ctx, blah, plop, test):
#     """
#     Click test command
#     """
#     collection = ctx.obj['collection']
#     click.secho("\nThis is just a test command.\n", fg="green")
#     click.secho(f"\n`{ctx.obj['collection']}`.\n", fg="green")
#     click.secho(f"\n`{collection}`.\n", fg="green")
#     # raise click.Abort()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter

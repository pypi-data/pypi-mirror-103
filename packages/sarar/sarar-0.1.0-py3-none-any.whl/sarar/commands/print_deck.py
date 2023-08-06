"""
print-deck command
"""

import pprint
from typeguard import typechecked  # see https://github.com/agronholm/typeguard
import click

import ruamel.yaml as yaml

pp = pprint.PrettyPrinter(indent=4)


@typechecked
def print_deck(deck_path: str):
    """
    Prints the given .deck file if it has a valid YAML syntax and has a valid SARAR Architecture.

    - See https://yaml.org/ for more details about the YAML syntax (YAML 1.2 should be supported).

    - See https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture/ for more details
      about the SARAR Architecture.

    :param deck_path: str: path to the .deck file to print
    :raises Exception: click: exception thrown if the YAML syntax of the .deck file is not valid
    """
    with open(deck_path) as stream:
        try:
            data = yaml.safe_load(stream)
            pp.pprint(data)
        except yaml.YAMLError as exc:
            click.secho(
                f"The .deck file `{deck_path}` cannot be parsed and printed, because its YAML "
                f"syntax is not valid! Check it, e.g. on https://yamlchecker.com/",
                fg="red",
            )
            click.secho(f"{exc}", fg="red")
            raise click.ClickException("\nSARAR is now stopped") from exc

"""
check-deck command
"""

from datetime import datetime
from asteval import Interpreter
import click
import ruamel.yaml as yaml
from typeguard import typechecked  # see https://github.com/agronholm/typeguard
import pycron
from sarar.decorators import emptychecked

aeval = Interpreter()

mandatory_deck_items = [
    "name",
    "cards",
]
options_keys = [
    "initial-interval",
    "max-interval",
    "min-interval",
    "review-window",
    "max-reviews-per-review-window",
    "max-new-cards-per-review-window",
    "review-wrong-card-until-right",
    "wrong-card-specific-interval",
    "print-tags-on-front",
    "print-tags-on-back",
    "card-answers",
]
card_keys = [
    "front",
    "back",
    "tags",
    "last-review",
    "interval",
    "is-wrong",
]
mandatory_card_keys = [
    "front",
]
card_answer_list_members = [
    "name",
    "new-card-interval",
    "is-wrong",
]
mandatory_card_answer_keys = [
    "name",
    "new-card-interval",
]

boolean_keys = [
    "print-tags-on-front",
    "print-tags-on-back",
    "review-wrong-card-until-right",
    "is-wrong",
]
integer_keys = [
    "max-reviews-per-review-window",
    "max-new-cards-per-review-window",
]
string_keys = [
    "name",
    "front",
    "back",
]
date_keys = [
    "last-review",
]
duration_keys = [
    "initial-interval",
    "max-interval",
    "min-interval",
    "wrong-card-specific-interval",
    "new-card-interval",
    "interval",
]
cron_keys = [
    "review-window",
]

replacers = {
    "initial-interval": "1",  #
    "max-interval": "1",  #
    "min-interval": "1",  #
    "interval": "1",  # intervals are replaced by 1 just in order to ease checking
    "years": "*60*60*24*365",
    "year": "*60*60*24*365",
    "months": "*60*60*24*30",
    "month": "*60*60*24*30",
    "weeks": "*60*60*24*7",
    "week": "*60*60*24*7",
    "days": "*60*60*24",
    "day": "*60*60*24",
    "hours": "*60*60",
    "hour": "*60*60",
    "minutes": "*60",
    "minute": "*60",
    "seconds": "*1",
    "second": "*1",
}

accepted_booleans = [
    True,
    "True",
    "true",
    "TRUE",
    1,
    "1",
    "Yes",
    "yes",
    "YES",
    "y",
    "Y",
    False,
    "False",
    "false",
    "FALSE",
    0,
    "0",
    "No",
    "no",
    "NO",
    "n",
    "N",
]


@typechecked
@emptychecked
def check_deck(deck_path: str):
    """
    Checks if the given .deck file has a valid YAML syntax and has a valid SARAR Architecture.

    - See https://yaml.org/ for more details about the YAML syntax (YAML 1.2 should be supported).

    - See https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture/ for more details
      about the SARAR Architecture.

    :param deck_path: str: path to the .deck file to check
    :raises exception: click: thrown if the YAML or SARAR syntax of the .deck file is not valid
    """

    # parse YAML content from .deck file in order to retrieve its data
    with open(deck_path) as stream:
        try:
            data = yaml.safe_load(stream)

            # check presence of mandatory items in a deck:
            check_mandatory_items_in_deck(deck_path, data)

            # check `name`, `deck` and `cards` content, and also check unknown item(s)
            for item in data:
                if item == "name":
                    pass
                elif item == "options":
                    check_options(deck_path, options=data["options"])
                elif item == "cards":
                    check_cards(deck_path, cards=data["cards"])
                else:
                    click.secho(
                        f"The .deck file `{deck_path}` contains an unknown `{item}` item.\n"
                        f"Make sure your .deck file has a valid SARAR Architecture:\n"
                        f"https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                        fg="red",
                    )
                    raise click.ClickException("\nSARAR is now stopped")

        # handle parsing errors if any
        except yaml.YAMLError as exc:
            click.secho(f"{exc}", fg="red")
            click.secho(
                f""
                f"The .deck file `{deck_path}` cannot be parsed, because its YAML syntax "
                f"is not valid! Check it, e.g. on https://yamlvalidator.com/",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_mandatory_items_in_deck(deck_path: str, data: dict):
    """
    Checks the presence of the mandatory item(s) in a deck.

    :param deck_path: str: path to the .deck file being checked
    :param data: dict: top level YAML keys/values (items) of the .deck file
    :raises exception: click: thrown if a mandatory item isn't present
    """
    for item in mandatory_deck_items:
        if item not in data:
            click.secho(
                f"The .deck file `{deck_path}` does not contains the mandatory `{item}` item. "
                f"Make sure your .deck file has a valid SARAR Architecture:\n"
                f"https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_options(deck_path: str, options: dict):
    """
    Checks the content of the `options` dictionnary.

    :param deck_path: str: path to the .deck file being checked
    :param options: dict: dictionnary containing options keys/values
    """
    check_unknown_keys_in_options(deck_path, options)
    check_known_keys_in_options(deck_path, options)


@typechecked
@emptychecked
def check_unknown_keys_in_options(deck_path: str, options: dict):
    """
    Checks if any unknown key is in the `options` dictionnary.

    :param deck_path: str: path to the .deck file being checked
    :param options: dict: dictionnary containing options keys/values
    :raises exception: click: thrown if an unknown key is in the options dictionnary
    """
    for key in options:
        if key not in options_keys:
            click.secho(
                f"The .deck file `{deck_path}` contains an unknown `{key}` key in the "
                "`options` dictionnary.\n"
                "Make sure your .deck file has a valid SARAR Architecture:\n"
                "https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_known_keys_in_options(deck_path: str, options: dict):
    """
    Checks the content of the known keys of the `options` dictionnary.

    :param deck_path: str: path to the .deck file being checked
    :param options: dict: dictionnary containing options keys/values
    :raises exception: click: thrown if a field is not handled properly by sarar
    """
    for key in options:
        if key in boolean_keys:
            check_boolean_field(deck_path, key, options[key])
        elif key in integer_keys:
            check_integer_field(deck_path, key, options[key])
        elif key in duration_keys:
            check_duration_field(deck_path, key, options[key])
        elif key in cron_keys:
            check_cron_field(deck_path, key, options[key])
        elif key == "card-answers":
            check_card_answers_option(deck_path, options[key])
        else:
            click.secho(
                f"The .deck file `{deck_path}` contains a field `{key}` that is not handled "
                f"properly by sarar. Please create an issue here: "
                f"https://gitlab.com/stephane.tzvetkov/sarar/-/issues with this error message, in "
                f"order for sarar to be corrected asap.",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_card_answers_option(deck_path: str, card_answers: list):
    """
    Checks the content of the `card-answers` option.

    :param deck_path: str: path to the .deck file being checked
    :param card_answers: list: list of card-answer in the `card-answers` option
    :raises exception: click: thrown if a field is not handled properly by sarar
    """
    for card_answer in card_answers:
        check_unknown_key_presence_in_card_answer(deck_path, card_answer)
        check_mandatory_keys_presence_in_card_answer(deck_path, card_answer)
        for field_key in card_answer:
            if field_key in boolean_keys:
                check_boolean_field(deck_path, field_key, card_answer[field_key])
            elif field_key in string_keys:
                check_string_field(deck_path, field_key, card_answer[field_key])
            elif field_key in duration_keys:
                check_duration_field(deck_path, field_key, card_answer[field_key])
            else:
                click.secho(
                    f"The .deck file `{deck_path}` contains the card-answer "
                    f"`{card_answer['name']}` (in the card-answers option) with the field "
                    f"`{field_key}` which is not handled properly by sarar. Please create an "
                    f"issue here: https://gitlab.com/stephane.tzvetkov/sarar/-/issues with this "
                    f"error message, in order for sarar to be corrected asap.",
                    fg="red",
                )
                raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_unknown_key_presence_in_card_answer(deck_path: str, card_answer: dict):
    """
    Checks the presence of unknown key in a card-answer dictionnary.

    :param deck_path: str: path to the .deck file being checked
    :param card_answer: dict: dictionnary containing card-answer keys/values
    :raises exception: click: thrown if an unknown key is found in the card-answer dictionnary
    """
    for card_answer_key in card_answer:
        if card_answer_key not in card_answer_list_members:
            click.secho(
                f"The .deck file `{deck_path}` contains an unknown `{card_answer_key}` key"
                "in a `card-answer` sub-dictionnary of the `options` dictionnary.\n"
                "Make sure your .deck file has a valid SARAR Architecture:\n"
                "https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_mandatory_keys_presence_in_card_answer(deck_path: str, card_answer: dict):
    """
    Checks the mandatory presence of the some key(s) in a card-answer dictionnary.

    :param deck_path: str: path to the .deck file being checked
    :param card_answer: dict: dictionnary containing card-answer keys/values
    :raises exception: click: thrown if the `new-card-interval` key isn't in the card-answer dict
    """
    for mandatory_card_answer_key in mandatory_card_answer_keys:
        if mandatory_card_answer_key not in card_answer:
            click.secho(
                f"The .deck file `{deck_path}` does not contains the mandatory "
                f"`{mandatory_card_answer_key}` key in the `card-answer` sub-dictionnary of the "
                f"`options` dictionnary.\n"
                f"Make sure your .deck file has a valid SARAR Architecture:\n"
                f"https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_cards(deck_path: str, cards: list):
    """
    Checks the content of the cards list.

    :param deck_path: str: path to the .deck file being checked
    :param cards: list: cards of the deck
    """
    for card in cards:
        check_unknown_keys_in_card(deck_path, card)
        check_mandatory_keys_presence_in_card(deck_path, card)
        check_known_keys_in_card(deck_path, card)


@typechecked
@emptychecked
def check_unknown_keys_in_card(deck_path: str, card: dict):
    """
    Checks if an unknown key is in the card.

    :param deck_path: str: path to the .deck file being checked
    :param card: dict: a card of the deck
    :raises exception: click: thrown if an unknown key is in the deck
    """
    for key in card:
        if key not in card_keys:
            click.secho(
                f"The .deck file `{deck_path}` contains an unknown `{key}` key in a `card` "
                "dictionnary. Make sure your .deck file has a valid SARAR Architecture:\n"
                "https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_mandatory_keys_presence_in_card(deck_path: str, card: dict):
    """
    Checks the presence of the mandatory keys in a card.

    :param deck_path: str: path to the .deck file being checked
    :param card: dict: a card of the deck
    :raises exception: click: thrown if a mandatory key isn't present in the card
    """
    for mandatory_card_key in mandatory_card_keys:
        if mandatory_card_key not in card:
            click.secho(
                f"The .deck file `{deck_path}` does not contains the mandatory "
                f"`{mandatory_card_key}` key in one of its cards. "
                f"Make sure your .deck file has a valid SARAR Architecture:\n"
                f"https://sarar.readthedocs.io/en/latest/user-guide/sarar-architecture",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_known_keys_in_card(deck_path: str, card: dict):
    """
    Checks the content of the known keys of a `card` dictionnary.

    :param deck_path: str: path to the .deck file being checked
    :param card: dict: dictionnary containing card's keys/values
    :raises exception: click: thrown if a field is not handled properly by sarar
    """
    for card_key in card.keys():
        if card_key in boolean_keys:
            check_boolean_field(deck_path, card_key, card[card_key])
        elif card_key in integer_keys:
            check_integer_field(deck_path, card_key, card[card_key])
        elif card_key in string_keys:
            check_string_field(deck_path, card_key, card[card_key])
        elif card_key in date_keys:
            check_date_field(deck_path, card_key, card[card_key])
        elif card_key in duration_keys:
            check_duration_field(deck_path, card_key, card[card_key])
        elif card_key == "tags":
            for tag in card["tags"]:
                check_string_field(deck_path, card_key, tag)
        else:
            click.secho(
                f"The .deck file `{deck_path}` contains a field `{card_key}` that is not handled "
                f"properly by sarar. Please create an issue here: "
                f"https://gitlab.com/stephane.tzvetkov/sarar/-/issues with this error message, in "
                f"order for sarar to be corrected asap.",
                fg="red",
            )
            raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_boolean_field(deck_path: str, field_key: str, field_value):
    """
    Checks the value of a field, which should be a boolean.

    :param deck_path: str: path to the .deck file being checked
    :param field_key: str: the field key
    :param field_value: str: the field value
    :raises exception: click: thrown if the `field_value` is not valid
    """
    if field_value not in accepted_booleans:
        click.secho(
            f"The .deck file `{deck_path}` contains a bad value associated to the "
            f"`{field_key}` field. "
            f"The value `{field_value}` of this field could not be parsed and converted into a "
            f"boolean. Accepted values for booleans are 'True', 'true', 'TRUE', '1', 'False', "
            f"'FALSE', '0'.\n",
            fg="red",
        )
        raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_integer_field(deck_path: str, field_key: str, field_value):
    """
    Checks the value of a field, which should be an integer.

    :param deck_path: str: path to the .deck file being checked
    :param field_key: str: the field key
    :param field_value: str: the field value
    :raises exception: click: thrown if the `field_value` is not valid
    """
    if not isinstance(field_value, int):
        click.secho(
            f"The .deck file `{deck_path}` contains a bad value associated to the "
            f"`{field_key}` field. "
            f"The value `{field_value}` of this field could not be parsed and converted into a "
            f"integer.\n",
            fg="red",
        )
        raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_string_field(deck_path: str, field_key: str, field_value):
    """
    Checks the value of a field, which should be a string.

    :param deck_path: str: path to the .deck file being checked
    :param field_key: str: the field key
    :param field_value: str: the field value
    :raises exception: click: thrown if the `field_value` is not valid
    """
    try:
        str(field_value)
    except Exception as exc:
        click.secho(
            f"The .deck file `{deck_path}` contains a bad value associated to the "
            f"`{field_key}` field. "
            f"The value `{field_value}` of this field could not be parsed and converted into a "
            f"string.\n",
            fg="red",
        )
        raise click.ClickException("\nSARAR is now stopped") from exc


@typechecked
@emptychecked
def check_date_field(deck_path: str, field_key: str, field_value: str):
    """
    Checks the value of a field, which should be a date.

    :param deck_path: str: path to the .deck file being checked
    :param field_key: str: the field key
    :param field_value: str: the field value
    :raises exception: click: thrown if the `field_value` is not valid
    """
    try:
        datetime.strptime(field_value, "%Y/%m/%d %H:%M:%S %z")
    except Exception as exc:
        click.secho(
            f"The .deck file `{deck_path}` contains a bad value associated to the "
            f"`{field_key}` field. "
            f"The value `{field_value}` of this field could not be parsed and converted into a "
            f'date. The expected date format is "year/month/day hour:minute:second timezone", '
            f'e.g. "2000/01/01 01:01:01 +0000".\n',
            fg="red",
        )
        raise click.ClickException("\nSARAR is now stopped") from exc


@typechecked
@emptychecked
def check_duration_field(deck_path: str, field_key: str, field_value: str):
    """
    Checks the value of a field, which should a valid duration.

    :param deck_path: str: path to the .deck file being checked
    :param field_key: str: the field key
    :param field_value: str: the field value
    :raises exception: click: thrown if the `field_value` is not valid
    """
    expr = parse_and_replace_expression(field_value)
    aeval(expr)
    if len(aeval.error) > 0:
        errmsg = ""
        for err in aeval.error:
            errmsg = f"{errmsg}\n{err.get_error()}"
        errmsg = f"{errmsg}\n"
        click.secho(
            "Error:\n"
            f"The .deck file `{deck_path}` contains a bad value associated to the "
            f"`{field_key}` field. "
            f"The value `{field_value}` of this field could not be parsed and converted into a "
            f"duration because of the below error:\n"
            f"{errmsg}",
            fg="red",
        )
        raise click.ClickException("\nSARAR is now stopped")


@typechecked
@emptychecked
def check_cron_field(deck_path: str, field_key: str, field_value: str):
    """
    Checks the value of a field, which should a valid cron expression.

    :param deck_path: str: path to the .deck file being checked
    :param field_key: str: the field key
    :param field_value: str: the field value
    :raises exception: click: thrown if the `field_value` is not valid
    """
    try:
        pycron.is_now(field_value)
    except Exception as exc:
        click.secho(
            f"The .deck file `{deck_path}` contains a bad value associated to the `{field_key}` "
            f"field. "
            f"The value `{field_value}` of this field could not be parsed and converted into a "
            f"cron expression.\n",
            fg="red",
        )
        raise click.ClickException("\nSARAR is now stopped") from exc


@typechecked
@emptychecked
def parse_and_replace_expression(expr: str) -> str:
    """
    Parses a string, mathematical expression representing a duration, and replaces a set of
    key words by their associated number of seconds.

    :param expr: str: the expression to parse
    :returns: str: the parsed expression with key words replaced
    """
    for rep in replacers:
        if rep in expr:
            expr = expr.replace(rep, replacers[rep])
    return expr

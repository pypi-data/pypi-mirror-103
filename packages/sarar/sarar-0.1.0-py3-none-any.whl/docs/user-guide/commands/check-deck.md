# check-deck

## NAME

check-deck

## SYNOPSIS

sarar check-deck [-d | --deck-path] [-h | help]

## DESCRIPTION

This command will check the YAML syntax and the SARAR architecture of the `.deck` file passed with
the below `-d, --deck-path` option. If no option is passed, this command will check all the decks
of the collection specified in your SARAR configuration file. And if no collection has been
defined, this command will throw an error.

See <https://yaml.org/> for more details about the YAML syntax.

See
<https://gitlab.com/stephane.tzvetkov/sarar/-/blob/master/docs/user-guide/sarar-architecture.md>
for more details about the SARAR architecture.

## OPTIONS

-d, --deck-path <PATH>
    <br/>
    Path to the deck to check.


-h, --help
    <br/>
    Show this message and exit.

## EXAMPLES

Check a specific deck:
    <br/>
    `#!Bash $ sarar check-deck -d /path/to/your/deck-file.deck`


Check all decks of your collection:
    <br/>
    `#!Bash $ sarar check-deck`

## LICENSE

License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.

This is free software: you are free to change and redistribute it. There is NO WARRANTY, to the
extent permitted by law.

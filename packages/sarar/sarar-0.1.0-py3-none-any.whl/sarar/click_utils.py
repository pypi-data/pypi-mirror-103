"""
Click custom utility classes.
"""

from click import Option, UsageError


class MutuallyExclusiveOption(Option):
    """
    This class defines mutualy exclusive options for Click:
    https://stackoverflow.com/questions/37310718/mutually-exclusive-option-groups-in-python-click
    """

    def __init__(self, *args, **kwargs):
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        # Hide auto include in help:
        # ##########################
        # hlp = kwargs.get('help', '')
        # if self.mutually_exclusive:
        #    ex_str = ', '.join(self.mutually_exclusive)
        #    kwargs['help'] = hlp + (
        #        ' NOTE: This argument is mutually exclusive with '
        #        ' the following options: [' + ex_str + '].'
        #    )
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            first_mutually_exclusive = "--" + self.name.replace("hlp", "help").replace("_", "-")
            next_mutually_exclusives = "--" + (
                ", --".join(self.mutually_exclusive).replace("hlp", "help").replace("_", "-")
            )
            raise UsageError(
                f"Illegal usage: option `{first_mutually_exclusive}` is mutually exclusive with "
                f"the following option(s) `{next_mutually_exclusives}`."
            )

        return super().handle_parse_result(ctx, opts, args)


class Map(dict):
    """
    This class allow to access the CONTEXT_SETTINGS outside of the Click framework:
    https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    self[key] = value

        if kwargs:
            for key, value in kwargs.items():
                self[key] = value

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super().__delitem__(key)
        del self.__dict__[key]

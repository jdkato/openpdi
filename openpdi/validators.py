"""OpenPDI - Cell Validators
"""
from datetime import datetime


VALIDATORS = {}


class VALIDATOR(object):
    """VALIDATOR keeps track of all the ``@VALIDATOR`` functions.
    """

    def __init__(self, f):
        VALIDATORS[f.__name__] = f


@VALIDATOR
def date(row, index, specifier):
    """Convert the given date to YYYY-MM-DD format.
    """
    try:
        value = row[index].split(" ")[0]
        return datetime.strptime(value, specifier).date()
    except ValueError as e:
        # TODO: Logging
        return None


@VALIDATOR
def raw(row, index, raw):
    """Return a pre-specified value instead of ``row[index]``.
    """
    return raw


@VALIDATOR
def time(row, index, specifier):
    """Convert the given time to 24-hour time in HH:MM format.
    """
    try:
        value = row[index]
        return datetime.strptime(value, specifier).strftime("%H:%M")
    except ValueError as e:
        return None


@VALIDATOR
def race(row, index):
    """Determine the race given by the specified column.

    TODO: Do this better ...
    """
    value = row[index].upper()
    if len(value) > 2:
        return value
    elif value == "W":
        return "WHITE"
    elif value == "B":
        return "BLACK"
    elif value == "H":
        return "HISPANIC"
    return None


@VALIDATOR
def lower(row, index):
    """Convert ``value`` to lower case.
    """
    return row[index].lower().strip()


@VALIDATOR
def upper(row, index):
    """Convert ``row[index]`` to upper case.
    """
    return row[index].upper().strip()


@VALIDATOR
def boolean(row, index):
    """Convert ``row[index]`` to a boolean value.

    TODO: Handle more than "Y/y".
    """
    return row[index].lower().startswith("y")


@VALIDATOR
def number(row, index):
    """Convert ``row[index]`` to a numerical value.
    """
    value = row[index]
    if not any(s.isdigit() for s in value):
        return value
    elif value.isdigit():
        return int(value)
    return float(value)


@VALIDATOR
def condition(row, index):
    """Convert ``row[index]`` to a standarized condition.

    TODO: spaCy-powered labels -- e.g., "DRUG"
    """
    return row[index].lower()


@VALIDATOR
def capitalize(row, index):
    """Return a capitalized version of ``row[index]``.
    """
    return row[index].capitalize()


@VALIDATOR
def sex(row, index):
    """Determine the sex given by the specified column.
    """
    value = row[index]
    if value.lower().startswith("m"):
        return "MALE"
    elif value.lower().startswith("f"):
        return "FEAMLE"
    return None

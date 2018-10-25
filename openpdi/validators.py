"""OpenPDI - Cell Validators
"""
import datetime

import pytz
import us

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
        return datetime.datetime.strptime(value, specifier).date()
    except ValueError as e:
        # TODO: Logging
        return None


@VALIDATOR
def raw(row, index, raw):
    """Return a pre-specified value instead of ``row[index]``.
    """
    return raw


@VALIDATOR
def time(row, index, state, specifier):
    """Convert the given time to 24-hour (UTC), HH:MM:SS format.

    TODO: tests
    """
    try:
        value = row[index]
        zones = us.states.lookup(state).time_zones
        naive = datetime.datetime.strptime(value, specifier)

        tz = pytz.timezone(zones[0])
        dt = tz.localize(naive, is_dst=None)
        return dt.astimezone(pytz.utc).strftime("%H:%M:%S")
    except ValueError as e:
        print(e)
        return None


@VALIDATOR
def race(row, index):
    """Determine the race given by the specified column.

    TODO: Handle cases like "W" -> "White".
    """
    value = row[index]
    return value.lower()


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
        return "male"
    elif value.lower().startswith("f"):
        return "female"
    return None

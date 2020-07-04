"""OpenPDI - Cell Validators
"""
import datetime

import us
import xlrd


VALIDATORS = {}


class VALIDATOR(object):
    """VALIDATOR keeps track of all the ``@VALIDATOR`` functions.
    """

    def __init__(self, f):
        VALIDATORS[f.__name__] = f


def _read_value(cell):
    """Read the value from the given cell.
    """
    if type(cell) != str:
        # We're dealing with a cell from either openpyxl or xlrd.
        if cell.value:
            return str(cell.value)
        return ""
    return cell


@VALIDATOR
def date(row, index, specifier):
    """Convert the given date to YYYY-MM-DD format.
    """
    value = _read_value(row[index]).split(" ")[0]
    if "T" in value:
        value = value.split("T")[0]

    try:
        d = datetime.datetime.strptime(value, specifier)
        return d.strftime("%Y-%m-%d")
    except ValueError:
        return None


@VALIDATOR
def raw(row, raw):
    """Return a pre-specified value instead of ``row[index]``.
    """
    return raw


@VALIDATOR
def none(row, index):
    """Return the unprocessed value instead of ``row[index]``.
    """
    return _read_value(row[index])


@VALIDATOR
def time(row, index, specifier):
    """Convert the given time to 24-hour time in HH:MM format.
    """
    try:
        value = _read_value(row[index])
        if "." in value:
            # We're probably dealing with an xlrd fraction:
            t = xlrd.xldate_as_tuple(float(value), 0)
            d = datetime.time(*t[3:])
        else:
            if "T" in value:
                value = value.split("T")[1]
            d = datetime.datetime.strptime(value, specifier)
        return d.strftime("%H:%M")
    except ValueError:
        return None


@VALIDATOR
def ethnicity(row, index):
    """
    """
    value = _read_value(row[index]).lower().strip(".")
    if value in ("nh", "non-hisp", "non - hisp"):
        return "NON-HISPANIC"
    return "HISPANIC"


@VALIDATOR
def race(row, index):
    """Determine the race given by the specified column.

    TODO: Do this better ...
    """
    value = _read_value(row[index]).upper()
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
    return _read_value(row[index]).lower().strip()


@VALIDATOR
def upper(row, index):
    """Convert ``row[index]`` to upper case.
    """
    return _read_value(row[index]).upper().strip()


@VALIDATOR
def boolean(row, index):
    """Convert ``row[index]`` to a boolean value.
    """
    value = _read_value(row[index]).lower()
    if value.startswith("y") or value.startswith("t"):
        return True
    return False


@VALIDATOR
def number(row, index):
    """Convert ``row[index]`` to a numerical value.

    TODO: Should we need to convert via `float` / `int`?
    """
    return _read_value(row[index])


@VALIDATOR
def condition(row, index):
    """Convert ``row[index]`` to a standarized condition.

    TODO: spaCy-powered labels -- e.g., "DRUG"
    """
    return _read_value(row[index]).lower()


@VALIDATOR
def capitalize(row, index):
    """Return a capitalized version of ``row[index]``.
    """
    return _read_value(row[index]).capitalize()


@VALIDATOR
def state(row, index):
    """Return the two-letter code for the given state.
    """
    value = _read_value(row[index])

    state = us.states.lookup(value)
    if state:
        return state.abbr
    return value


@VALIDATOR
def sex(row, index):
    """Determine the sex given by the specified column.
    """
    value = _read_value(row[index]).lower()
    if value.startswith("m"):
        return "MALE"
    elif value.startswith("f"):
        return "FEMALE"
    return None

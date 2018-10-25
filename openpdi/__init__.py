# -*- coding: utf-8 -*-

"""
OpenPDI
~~~~~~~

OpenPDI is a Python library for working with data submitted to the Police Data
Initiative.

Usage:
    >>> import openpdi
    # Load the "uof" dataset, including only sources that an "officer_sex"
    # column.
    >>> openpdi.write('uof', with_cols=['officer_sex'])

Full documentation is available at <https://openpdi.com/docs>.

:copyright: (c) 2018 Joseph Kato.
:license: MIT, see LICENSE for more details.
"""
import csv
import io
import json
import logging
import os
import pathlib

import openpyxl
import requests
import tqdm

from itertools import islice
from openpdi.validators import VALIDATORS

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = pathlib.Path(os.path.join(FILE_PATH, "meta"))


def _fetch(url, f_type="csv"):
    """Fetch the provided resource, ``url``, and return a ``Dataset``.

    ``url`` may link to data in XLSX, CSV, or TSV format.
    """
    iterator = iter([])

    r = requests.get(url, allow_redirects=True)
    if f_type == "csv":
        csvfile = io.StringIO(r.text)
        dialect = csv.Sniffer().sniff(csvfile.read(1024))
        csvfile.seek(0)
        iterator = csv.reader(csvfile, dialect)

    for row in islice(iterator, 1, None):
        yield row


def _read_meta(path):
    """
    """
    with open(path) as meta:
        return json.load(meta)


def _merge(f_obj, headers, sources, formats):
    """
    """
    writer = csv.writer(f_obj, delimiter=",", quoting=csv.QUOTE_ALL)

    writer.writerow(headers)
    for source in tqdm.tqdm(sources):
        for row in _fetch(source["url"]):
            made = []
            for header in headers:
                if header in source["columns"]:
                    v = VALIDATORS.get(formats[header])
                    made.append(v(row, **source["columns"][header]))
                else:
                    made.append(None)
            writer.writerow(made)


def write(dataset, f_obj, with_cols=[], strict=False):
    """Load the given dataset.

    A "dataset" is a collection of data related to a particular topic -- e.g.,
    the "uof" ("Use of Force) dataset contains data from a number of different
    police departments around the country.

    Args:
        ``dataset``: The name of the dataset (e.g., "uof").
        ``with_cols``: A list specifying columns that must be included.
        ``strict``: If true, only report columns specified in ``with_cols``.

    Examples:
        >>> import openpdi
        # Load the "uof" dataset, including only sources that an "officer_sex"
        # column.
        >>> openpdi.write("uof", with_cols=["officer_sex"])
    """
    schema = _read_meta(DATA_PATH.joinpath(dataset, "schema.json"))

    formats = {}
    for entry in schema["fields"]:
        formats[entry["label"]] = entry["format"]

    columns, sources = set(), []
    for f in DATA_PATH.glob("**/meta.json"):
        for meta in _read_meta(f):
            sample_cols = meta["columns"]
            if not all(h in sample_cols for h in with_cols):
                continue
            elif strict:
                columns.update(with_cols)
            else:
                columns.update(sample_cols)
            sources.append(meta)

    return _merge(f_obj, sorted(columns), sources, formats)

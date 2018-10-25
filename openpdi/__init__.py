# -*- coding: utf-8 -*-

"""
OpenPDI
~~~~~~~

OpenPDI is a Python library and command-line tool for working with data
submitted to the Police Data Initiative.

Usage:
    >>> import openpdi
    # Load the "uof" dataset, including only sources that an "officer_sex"
    # column.
    >>> dataset = openpdi.load("uof", with_cols=["officer_sex"])

Full documentation is available at <https://openpdi.com/docs>.

:copyright: (c) 2018 Joseph Kato.
:license: MIT, see LICENSE for more details.
"""
import csv
import json
import os
import pathlib

import pygogo as gogo
import requests
import tablib
import tqdm

from collections import OrderedDict
from typing import Dict, List

from openpdi.validators import VALIDATORS

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = pathlib.Path(os.path.join(FILE_PATH, "meta"))


def _fetch(url: str) -> tablib.Dataset:
    """Fetch the provided resource, ``url``, and return a ``Dataset``.

    ``url`` may link to data in XLSX, CSV, JSON, TSV, or ODS format.
    """
    try:
        r = requests.get(url, allow_redirects=True)
        r.raise_for_status()
        return tablib.Dataset().load(r.text)
    except Exception as err:
        # TODO: pygogo logging
        print(err)
    return None


def _read_meta(path: str) -> Dict:
    """
    """
    with open(path) as meta:
        return json.load(meta)


def _merge(headers: str, data: List[Dict], formats: Dict[str, str]) -> tablib.Dataset:
    """
    """
    output = tablib.Dataset()
    output.headers = headers

    for entry in data:
        for row in entry["ds"]:
            made = []
            for header in output.headers:
                if header in entry["columns"]:
                    validator = VALIDATORS.get(formats[header])
                    made.append(validator(row, **entry["columns"][header]))
                else:
                    made.append(None)
            output.rpush(made)

    return output


def load(dataset: str, with_cols: List[str] = []) -> tablib.Dataset:
    """Load the given dataset.

    A "dataset" is a collection of data related to a particular topic -- e.g.,
    the "uof" ("Use of Force) dataset contains data from a number of different
    police departments around the country.

    Args:
        ``dataset``: The name of the dataset (e.g., "uof").
        ``with_cols``: A list specifying columns that must be included.

    Returns:
        An instace of ``tablib.Dataset`` containing the user-specified data
        sources.

    Examples:
        >>> import openpdi
        # Load the "uof" dataset, including only sources that an "officer_sex"
        # column.
        >>> dataset = openpdi.load("uof", with_cols=["officer_sex"])
    """
    schema = _read_meta(DATA_PATH.joinpath(dataset, "schema.json"))

    formats = {}
    for entry in schema["fields"]:
        formats[entry["label"]] = entry["format"]

    columns, datasets = set(), []
    for f in DATA_PATH.glob("**/meta.json"):
        for meta in _read_meta(f):
            sample_cols = meta["columns"]
            if not all(h in sample_cols for h in with_cols):
                continue
            datasets.append({"ds": _fetch(meta["url"]), "columns": sample_cols})
            for k in sample_cols:
                columns.add(k)

    return _merge(sorted(columns), datasets, formats)

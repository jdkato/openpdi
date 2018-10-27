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
import os
import pathlib

import openpyxl
import requests
import tqdm
import xlrd

from openpdi.validators import VALIDATORS

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
DATA_PATH = pathlib.Path(os.path.join(FILE_PATH, "meta"))


def _read_csv(text, start):
    """
    """ 
    csvfile = io.StringIO(text)
    dialect = csv.Sniffer().sniff(csvfile.readline())
    return csv.reader(csvfile, dialect)


def _read_xlsx(text, start):
    """
    """ 
    wb = openpyxl.load_workbook(filename=io.BytesIO(text), read_only=True)
    return wb.worksheets[0].iter_rows(min_row=start)


def _read_xlrd(text, start):
    """
    """ 
    wb = xlrd.open_workbook(file_contents=text)

    rows = wb.sheet_by_index(0).get_rows()
    for _ in range(start):
        next(rows)

    return rows


def _fetch(meta):
    """Fetch the provided resource, ``url``, and return a ``Dataset``.

    ``url`` may link to data in XLSX, CSV, or TSV format.
    """
    r = requests.get(meta["url"], allow_redirects=True)
    iterator = iter([])

    f_type = meta["type"]
    if f_type == "csv":
        iterator = _read_csv(r.text, meta.get("start"))
    elif f_type == "xlsx":
        iterator = _read_xlsx(r.content, meta.get("start"))
    elif f_type == "xlrd":
        iterator = _read_xlrd(r.content, meta.get("start"))

    for row in iterator:
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
        for row in _fetch(source):
            made = []
            for header in headers:
                if header in source["columns"]:
                    v = VALIDATORS.get(formats[header])
                    made.append(v(row, **source["columns"][header]))
                else:
                    made.append(None)
            writer.writerow(made)


def write(dataset, f_obj, columns=[], strict=False, location=None):
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

    headers, sources = set(), []
    for f in DATA_PATH.glob("**/meta.json"):
        if location and location not in str(f.absolute()):
            continue
        for meta in _read_meta(f):
            sample_cols = meta["columns"]
            if not all(h in sample_cols for h in columns):
                continue
            elif strict:
                headers.update(columns)
            else:
                headers.update(sample_cols)
            sources.append(meta)

    return _merge(f_obj, sorted(headers), sources, formats)

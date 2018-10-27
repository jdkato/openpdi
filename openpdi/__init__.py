# -*- coding: utf-8 -*-

"""
OpenPDI
~~~~~~~

OpenPDI is a Python library for working with data submitted to the Police Data
Initiative.

The idea is to provide arbitrary access to data from disparate sources. In
other words, given a particular topic (e.g., "Use of Force"), we want to allow
researchers to automate the process of creating standardized data sets.

Usage:
    >>> import openpdi
    # Load the "uof" data set, including only sources that include an
    # "subject_race" column.
    >>> with open('uof.csv', 'w+') as csvfile:
            openpdi.write(
                'uof',
                csvfile,
                columns=['subject_race'],
                location='TX/Austin')

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


def write(topic, f_obj, columns=[], strict=False, location=None):
    """Create a data set from the given constraints.

    Args:
        topic: The name of the particular data set (e.g., "uof").

        f_obj: a file-like object to write the data set to.

        columns: A list specifying columns that must be included. For example,
                 our analysis might require that the ``officer_race`` column is
                 included in any data source we consider.

        strict: If true, only columns specified in ``columns`` will be reported
                in the final data set.

        location: A string (in the form "state/city") specifying a certain
                  location to limit results to -- e.g., "TX/Dallas".
    """
    schema = _read_meta(DATA_PATH.joinpath(topic, "schema.json"))

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


def _read_csv(text, start):
    """Read the given string (``text``) as a CSV file.
    """
    csvfile = io.StringIO(text)
    dialect = csv.Sniffer().sniff(csvfile.readline())

    reader = csv.reader(csvfile, dialect)
    for _ in range(start - 1):
        # NOTE: we use 'start - 1' because we've already read the first line
        # (see above).
        next(reader)

    return reader


def _read_xlsx(text, start):
    """Read the given string (``text``) as an .xlsx file (Excel 2010+).
    """
    wb = openpyxl.load_workbook(filename=io.BytesIO(text), read_only=True)
    return wb.worksheets[0].iter_rows(min_row=start)


def _read_xlrd(text, start):
    """Read the given string (``text``) as an .xls file.
    """
    wb = xlrd.open_workbook(file_contents=text)

    rows = wb.sheet_by_index(0).get_rows()
    for _ in range(start):
        next(rows)

    return rows


def _fetch(meta):
    """Fetch the provided resource, ``url``.
    """
    r = requests.get(meta["url"], allow_redirects=True)
    iterator = iter([])

    f_type, start = meta["type"], meta["start"]
    if f_type == "csv":
        iterator = _read_csv(r.text, start)
    elif f_type == "xlsx":
        iterator = _read_xlsx(r.content, start)
    elif f_type == "xlrd":
        iterator = _read_xlrd(r.content, start)

    for row in iterator:
        yield row


def _read_meta(path):
    """Read a meta (JSON) file.
    """
    with open(path) as meta:
        return json.load(meta)


def _merge(f_obj, headers, sources, formats):
    """Merge multiple data sources into a single CSV file (``f_obj``).
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

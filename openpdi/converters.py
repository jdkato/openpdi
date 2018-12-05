import csv
import io

import openpyxl
import requests
import xlrd


def fetch(meta):
    """Fetch the provided resource, `url`.
    """
    # TODO: To avoid reading the entire file into memory, should we use
    # `stream=True`?
    r = requests.get(meta["url"], allow_redirects=True)
    iterator = None

    f_type, start = meta["type"], meta["start"]
    if f_type == "csv":
        iterator = _read_csv(r.text, start)
    elif f_type == "xlsx":
        iterator = _read_xlsx(r.content, start)
    else:
        iterator = _read_xlrd(r.content, start)

    for row in iterator:
        yield row


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

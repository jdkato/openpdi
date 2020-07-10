# OpenPDI [![Build Status](https://travis-ci.org/OpenPDI/openpdi.svg?branch=master)](https://travis-ci.org/OpenPDI/openpdi) [![code style](https://img.shields.io/badge/code%20style-black-%23000.svg)](https://github.com/OpenPDI/openpdi) [![DOI](https://zenodo.org/badge/153943607.svg)](https://zenodo.org/badge/latestdoi/153943607) [![PyPI - Python Version](https://img.shields.io/pypi/pyversions/openpdi)](https://pypi.org/project/openpdi/)

OpenPDI is an unofficial effort to document and standardize data submitted to
the [Police Data Initiative][3] (PDI). The goal is to make the data more accessible
by addressing a number of issues related to a lack of
standardization&mdash;namely,

- **File types**: While some agencies make use if the
  [Socrata Open Data API](https://dev.socrata.com/), many provide their data
  in raw `.csv`, `.xlsx`, or `.xls` files of varying structures.
- **Column names**: Many columns that represent the same data (e.g., the race
  police officer) are named differently across departments, cities, and states.
- **Value formats**: Dates, times, and other comparable fields are submitted in
  many different formats.
- **Column availability**: It's currently very difficult to identify data
  sources that contain certain columns&mdash;e.g., *Use of Force* data
  specifying the hire date of the involved officer(s).

## Getting Started

###### Installation

```shell
$ pip install openpdi
```

###### Usage

| Dataset           | ID    | Source                                                      |
|-------------------|-------|-------------------------------------------------------------|
| [Use of Force][1] | `uof` | https://www.policedatainitiative.org/datasets/use-of-force/ |

```python
import csv
import openpdi

# The library has a single entry point:
dataset = openpdi.Dataset(
    # The dataset ID (see the table above).
    "uof",
    # Limit the data sources to a specific state using its two-letter code.
    #
    # Default: `scope=[]`.
    scope=["TX"],
    # A list of columns that must be provided in every data source included in
    # this dataset. See `openpdi/meta/{ID}/schema.json` for the available
    # columns.
    #
    # Default: `columns=[]`.
    columns=["reason"],
    # If `True`, only return the user-specified columns -- i.e., those listed
    # in the `columns` parameter.
    #
    # Default: `strict=False`.
    strict=False)

# The names of the agencies included in this dataset:
print(dataset.agencies)

# The URLs of the external data sources inlcuded in this dataset:
print(dataset.sources)

# `gen` is a generator object for iterating over the CSV-formatted dataset.
gen = dataset.download()

# Write to a CSV file:
with open("dataset.csv", "w+") as f:
    writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
    writer.writerows(gen)
```

## Datasets

In an attempt to avoid unnecessary bloat (in terms of GBs), we don't actually store any PDI data in this repository. Instead, we store small, JSON-formatted descriptions of externally hosted datasets&mdash;for example, [`uof/CA/meta.json`](https://github.com/OpenPDI/openpdi/blob/master/openpdi/meta/uof/CA/meta.json):

```json
[
    {
        "url": "https://www.norwichct.org/Archive.aspx?AMID=61&Type=Recent",
        "type": "csv",
        "start": 1,
        "columns": {
            "date": {
                "index": 0,
                "specifier": "%m/%d/%Y"
            },
            "city": {
                "raw": "Richmond"
            },
            "state": {
                "raw": "CA"
            },
            "service_type": {
                "index": 1
            },
            "force_type": {
                "index": 10
            },
            "light_conditions": {
                "index": 8
            },
            "weather_conditions": {
                "index": 7
            },
            "reason": {
                "index": 2
            },
            "officer_injured": {
                "index": 6
            },
            "officer_race": {
                "index": 9
            },
            "subject_injured": {
                "index": 5
            },
            "aggravating_factors": {
                "index": 3
            },
            "arrested": {
                "index": 4
            }
        }
    }
]
```

This file describes a Use of Force (`uof`) dataset from Richmond, CA. Each entry in the `columns` array maps a column from the externally-hosted data to a column in the dataset's schema file ([`uof/schema.json`](https://github.com/OpenPDI/openpdi/blob/master/openpdi/meta/uof/schema.json)).

![flow][4]

The `schema.json` file assigns a `format` to every possible column in a particular dataset, which is a Python function tasked with standardizing a raw column value (see [`openpdi/validators.py`](https://github.com/OpenPDI/openpdi/blob/master/openpdi/validators.py)).

[1]: https://github.com/jdkato/OpenPDI/tree/master/openpdi/meta/uof
[2]: https://www.policedatainitiative.org/datasets/use-of-force/
[3]: https://www.policedatainitiative.org/
[4]: https://user-images.githubusercontent.com/8785025/49119503-6975ac80-f25d-11e8-9310-802492815b39.png

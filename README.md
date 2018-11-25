# OpenPDI [![Build Status](https://travis-ci.org/OpenPDI/openpdi.svg?branch=master)](https://travis-ci.org/OpenPDI/openpdi) [![code style](https://img.shields.io/badge/code%20style-black-%23000.svg)](https://github.com/OpenPDI/openpdi) [![DOI](https://zenodo.org/badge/153943607.svg)](https://zenodo.org/badge/latestdoi/153943607) [![Thanks](https://img.shields.io/badge/say-thanks-ff69b4.svg?&amp;logo=gratipay&amp;logoColor=white)](#say-thanks)


OpenPDI is an unofficial effort to document and standardize data submitted to
the [Police Data Initiative][3] (PDI). The goal is to make the data more accessible
by addressing a number of issues related to a lack of
standardization&mdash;namely,

- **File types**: While some agencies make use if the
  [Socrata Open Data API](https://dev.socrata.com/), many provide their data
  in raw CSV or xlsx/xlsm files of varying structures.
- **Column names**: Many columns that represent the same data (e.g., the race
  police officer) are named differently across departments, cities, and states.
- **Value formats**: Dates, times, and other comparable fields are submitted in
  many different formats.
- **Column availability**: It's currently very difficult to identify data
  sources that contain certain columns&mdash;e.g., *Use of Force* data
  specifying the hire date of the involved officer(s).

You can learn more by reading the project's [mission statement](), [API docs](), or [Wiki]().

## Getting Started

###### Installation

```shell
$ pip install openpdi
```

###### Usage

```python
>>> import openpdi
# Find all data Use of Force datasets with a 'hire_date' column.
>>> dataset = openpdi.Dataset('uof', columns=['hire_date'])
>>> dataset.agencies
...
>>> gen = dataset.download()
# `gen` is a generator object for iterating over the CSV-formatted
# dataset.
>>> next(gen) # The headers
...
```

See the [API docs]() for more information.

[1]: https://github.com/jdkato/OpenPDI/tree/master/openpdi/meta/uof
[2]: https://www.policedatainitiative.org/datasets/use-of-force/
[3]: https://www.policedatainitiative.org/

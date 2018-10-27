# OpenPDI

OpenPDI is an unofficial effort to document and standardize data submitted to
the Police Data Initiative (PDI). The goal is to make the data more accessible
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

## Getting Started

```python
import openpdi

with open('uof.csv', 'w+') as csvfile:
    openpdi.write('uof', csvfile, with_cols=['longitude'])
```

| Data set     | ID    | Source                                                      |
|--------------|-------|-------------------------------------------------------------|
| Use of Force | `uof` | [`PDI/use-of-force`](https://www.policedatainitiative.org/datasets/use-of-force/) |

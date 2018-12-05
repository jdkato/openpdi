# -*- coding: utf-8 -*-

"""
"""
import json
import pathlib

import tabulate

from .converters import fetch
from .validators import VALIDATORS

_DATA_PATH = META = pathlib.Path(__file__).parents[1] / "openpdi" / "meta"


class Dataset(object):
    """Dataset represents an individual topic-specific dataset from the PDI.
    """

    def __init__(self, topic, scope=[], columns=[], strict=False):
        """Create a `Dataset` for `topic`.
        """
        schema_path = _DATA_PATH.joinpath(topic, "schema.json")
        assert schema_path.exists(), "Unknown dataset"

        schema = _read_meta(schema_path)

        self._headers = set()
        self._sources = []

        # The topic of the dataset.
        #
        # See the README for a list of available topics.
        self.topic = topic

        # The title of the dataset.
        self.title = schema["title"]

        # The standardized columns in this dataset.
        #
        # See the relevant `schema.json` file for descriptions of the avilable
        # standardized fields.
        self.columns = schema["fields"]

        # A list of agencies with data in this dataset.
        #
        # See the [PDI website](https://www.policedatainitiative.org/) for more
        # information.
        self.agencies = set()

        # The URLs of the external sources.
        self.sources = set()

        # The number of files in this dataset.
        self._size = 0

        for f in _DATA_PATH.glob("**/meta.json"):
            for meta in _read_meta(f):
                sample_cols = meta["columns"]

                state = meta["columns"]["state"]["raw"]
                agency = "{0}-{1}".format(
                    state, meta["columns"]["city"]["raw"]
                )

                if not all(h in sample_cols for h in columns):
                    continue
                elif scope and all(p not in scope for p in (state, agency)):
                    continue
                elif strict:
                    self._headers.update(columns)
                else:
                    self._headers.update(sample_cols)

                self._sources.append(meta)
                self._size += 1

                self.sources.add(meta["url"])
                self.agencies.add(agency)

    def __len__(self):
        return self._size

    def __repr__(self):
        return "Dataset({!r})".format(self.title)

    def __unicode__(self):
        return tabulate.tabulate(
            [[self.title, self.topic, str(self.__len__())]],
            ["Title", "ID", "Number of Agencies"],
            tablefmt="pipe",
        )

    def __str__(self):
        return self.__unicode__()

    def download(self):
        """Download the data for this dataset.
        """
        formats = {}
        for entry in self.columns:
            formats[entry["label"]] = entry["format"]

        yield from _merge(sorted(self._headers), self._sources, formats)


def _read_meta(path):
    """Read a meta (JSON) file.
    """
    with open(path) as meta:
        return json.load(meta)


def _merge(headers, sources, formats):
    """Merge multiple data sources into a single CSV file.
    """
    yield headers
    for source in sources:
        for row in fetch(source):
            made = []
            for header in headers:
                if header in source["columns"]:
                    v = VALIDATORS.get(formats[header])
                    made.append(v(row, **source["columns"][header]))
                else:
                    made.append(None)
            yield made

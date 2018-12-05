import json
import pathlib
import unittest

import jsonschema


DATA = pathlib.Path(__file__).parents[1] / "openpdi" / "meta"

SCHEMA = pathlib.Path(__file__).parents[0] / "schema.json"
META = pathlib.Path(__file__).parents[0] / "meta.json"


class SchemaTestCase(unittest.TestCase):
    """Ensure all schema.json files are valid.
    """

    def test_datasets(self):
        for f in DATA.glob("**/schema.json"):
            try:
                with f.open() as e, SCHEMA.open() as s:
                    jsonschema.validate(json.load(e), json.load(s))
            except jsonschema.ValidationError as e:
                self.fail(e)

    def test_data_sources(self):
        for f in DATA.glob("**/meta.json"):
            try:
                with f.open() as e, META.open() as s:
                    jsonschema.validate(json.load(e), json.load(s))
            except jsonschema.ValidationError as e:
                self.fail(e)


if __name__ == "__main__":
    unittest.main()

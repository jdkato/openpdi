import json
import pathlib
import unittest

import jsonschema


META = pathlib.Path(__file__).parents[1] / "openpdi" / "meta"
SCHEMA = pathlib.Path(__file__).parents[0] / "schema.json"


class SchemaTestCase(unittest.TestCase):
    """Ensure all schema.json files are valid.
    """

    def test_valid(self):
        for f in META.glob("**/schema.json"):
            try:
                with f.open() as e, SCHEMA.open() as s:
                    jsonschema.validate(json.load(e), json.load(s))
            except jsonschema.ValidationError as e:
                self.fail(e)


if __name__ == "__main__":
    unittest.main()

import json
import pathlib
import unittest

import requests


META = pathlib.Path(__file__).parents[1] / "openpdi" / "meta"


class LinksTestCase(unittest.TestCase):
    """Ensure all of our external data sources are working.
    """

    def test_get(self):
        for f in META.glob("**/meta.json"):
            with f.open() as meta:
                data = json.load(meta)
            for entry in data:
                r = requests.get(entry["url"], stream=True)
                code = r.status_code
                self.assertEqual(
                    code,
                    200,
                    msg="'{0}' has code '{1}'".format(entry["url"], code),
                )


if __name__ == "__main__":
    unittest.main()

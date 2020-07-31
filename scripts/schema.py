import json
import pathlib

import tabulate

data = pathlib.Path(__file__).parents[1] / "openpdi" / "meta" / "uof"

if __name__ == "__main__":
    schema_path = data.joinpath("schema.json")
    with open(schema_path, "r") as s:
        columns = json.load(s)

    rows = []
    for col in sorted(columns["fields"], key = lambda i: i["label"]):
        agencies = []
        for d in data.glob("*/*.json"):
            with open(d, "r") as a:
                for agency in json.load(a):
                    if col["label"] in agency["columns"]:
                        agencies.append(agency["url"].split("/")[-2])

        link = "[`{0}`](https://github.com/OpenPDI/data/releases/tag/{0})"
        rows.append([
            "`{0}`".format(col["label"]),
            col["description"],
            "`{0}`".format(col["example"].replace("|", "/")),
            ", ".join([link.format(f) for f in set(agencies)])
        ])

    table = tabulate.tabulate(
        rows,
        [
            "Column name",
            "Column description",
            "Example value",
            "Reporting Agencies"
        ],
        tablefmt="pipe",
    )

    print(table)

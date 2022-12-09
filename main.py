import json
from pathlib import Path

import fortiweb_conf_parser
import fortiweb_report


def main(config_file: str, xlxs_output: str, json_output: str):
    source_code = Path(config_file).read_text()
    stream = fortiweb_conf_parser.StreamHandler(source_code)
    data: dict = fortiweb_conf_parser.parse(stream)
    with open(json_output, 'w') as file:
        json.dump(data, file)
    fortiweb_report.generate(data, xlxs_output)


if __name__ == "__main__":
    main('data/C8ASPFIRACC.conf', 'data/matrice.xlsx', 'data/data.json')

import json
from pathlib import Path

import fortiweb_conf_parser
import generate_xlsx


def main(config_file: str, xlxs_output: str, json_output: str):
    source_code = Path(config_file).read_text()
    stream = fortiweb_conf_parser.StreamHandler(source_code)
    data: dict = fortiweb_conf_parser.parse(stream)
    with open(json_output, 'w') as file:
        json.dump(data, file)
    generate_xlsx.generate_from_files(json_output, xlxs_output)


if __name__ == "__main__":
    main('data/C8ASPFIRACC.conf', 'data/fortiweb_report.toml', 'data/data.json')

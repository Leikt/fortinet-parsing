import json
from pathlib import Path

import fortiweb_conf_parser


def main(config_file: str, output: str):
    source_code = Path(config_file).read_text()
    stream = fortiweb_conf_parser.StreamHandler(source_code)
    data: dict = fortiweb_conf_parser.parse(stream)
    with open(output, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main('data/C8ASPFIRACC.conf', 'data/parsed.json')

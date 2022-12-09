import json
from pathlib import Path

import fortinet_reporter


def main(config_file: str, output: str):
    source_code = Path(config_file).read_text()
    stream = fortinet_reporter.StreamHandler(source_code)
    data: dict = fortinet_reporter.parse(stream)
    with open(output, 'w') as file:
        json.dump(data, file)


if __name__ == "__main__":
    main('data/C8ASPFIRACC.conf', 'data/parsed.json')

import json
from pathlib import Path

import fortinet_reporter

source_code = Path('data/C8ASPFIRACC.conf').read_text()
stream = fortinet_reporter.StreamHandler(source_code)
data: list = fortinet_reporter.parse(stream)
with open('data/parsed.json', 'w') as file:
    json.dump(data, file)

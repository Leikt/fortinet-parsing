import json
from pathlib import Path

from fortinet_reporter.parser import parse
from fortinet_reporter.stream_handler import StreamHandler

source_code = Path('data/C8ASPFIRACC.conf').read_text()
stream = StreamHandler(source_code)
data: list = parse(stream)
with open('data/parsed.json', 'w') as file:
    json.dump(data, file)

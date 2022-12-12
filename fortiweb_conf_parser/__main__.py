import argparse
import json
from pathlib import Path

from fortiweb_conf_parser.parser import parse
from fortiweb_conf_parser.stream_handler import StreamHandler

parser = argparse.ArgumentParser(prog="Fortinet configuration parser")
parser.add_argument('config', type=Path,
                    help='Path to the configuration file to parse')
parser.add_argument('dest', type=Path,
                    help='Path to the output json file')
args = parser.parse_args()

source_code = args.config.read_text('utf-8')
stream = StreamHandler(source_code)
data = parse(stream)
args.dest.write_text(json.dumps(data), 'utf-8')

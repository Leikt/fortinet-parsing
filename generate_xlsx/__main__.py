import argparse
from pathlib import Path

from generate_xlsx.generate import generate_from_files

parser = argparse.ArgumentParser(prog="XLSX Generator")
parser.add_argument('-d', '--data', type=Path, required=True,
                    help='Path to the json file containing the data to report')
parser.add_argument('-c', '--config', type=Path, required=True,
                    help='Path to the toml file containing the xlsx configuration')
args = parser.parse_args()

generate_from_files(args.data, args.config)

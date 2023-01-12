import argparse
from pathlib import Path

from generate_xlsx.generate import generate_from_files

parser = argparse.ArgumentParser(prog="XLSX Generator")
parser.add_argument('config', type=Path,
                    help='Path to the toml file containing the xlsx configuration')
args = parser.parse_args()

generate_from_files(args.config)

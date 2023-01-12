import argparse
from pathlib import Path

from generate_xlsx.generate import generate_from_files, Glossary

parser = argparse.ArgumentParser(prog="XLSX Generator")
parser.add_argument('-d', '--data', type=Path, required=True,
                    help='Path to the json file containing the data to report')
parser.add_argument('-c', '--config', type=Path, required=True,
                    help='Path to the toml file containing the xlsx configuration')
parser.add_argument('-g', '--glossary', type=Path,
                    help='Path to the toml file containing the glossary')
args = parser.parse_args()

if args.glossary:
    Glossary.load(args.glossary)

generate_from_files(args.data, args.config)

import json
from os import PathLike
from pathlib import Path
from typing import Dict, List, Union, Optional

import toml
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from generate_xlsx.selectors import select_data


def generate_from_files(config_file: Union[str, PathLike]):
    """Generate the report using the data and configuration in the given files."""
    config = toml.loads(Path(config_file).read_text('utf-8'))
    _validate_config(config)

    data = json.loads(Path(config['general']['source']).read_text('utf-8'))

    glossary = config.get('glossary')
    if glossary is None:
        glossary = config['general'].get('glossary')
        if glossary is not None:
            glossary = toml.loads(Path(glossary).read_text('utf-8'))
    if glossary is not None:
        Glossary.set(glossary)

    generate(data, config)


def generate(data: dict, config: dict):
    """Generate a workbook using the configuration and the given data."""
    workbook = Workbook(config['general']['destination'])
    formats = _setup_formats(workbook, config.get('formats', {}))
    for ws in config['sheet']:
        name = ws['name']
        selector = ws['selector']
        selector_args = ws['selector_arguments']
        columns = _build_columns_info(ws['column'])
        _create_worksheet(select_data(selector, selector_args, data), workbook, formats, name, columns)
    workbook.close()


def _validate_config(config: dict):
    if 'general' not in config:
        raise ValueError("Config must have a 'general' section")

    if 'sheet' not in config:
        raise ValueError("Config must have at least one 'sheet' section")

    if 'source' not in config['general']:
        raise ValueError("Config must have general.source value")

    if 'destination' not in config['general']:
        raise ValueError("COnfig must have a general.destination value")


def _setup_formats(workbook: Workbook, formats_config: dict) -> Dict[str, Format]:
    """Load the configured formats into the workbook."""
    formats = {}
    for name, properties in formats_config.items():
        formats[name] = workbook.add_format(properties)
    return formats


def _build_columns_info(columns_config: list) -> list:
    """Retrieve information from the configuration and transform it to a usable value."""
    return [(col['name'], col['width'], col.get('source', None)) for col in columns_config]


def _create_worksheet(data: dict, workbook: Workbook, formats: dict, sheet_name: str, columns: List[tuple]):
    """Add a new worksheet to the given workbook."""
    worksheet = workbook.add_worksheet(sheet_name)
    _setup_columns(worksheet, columns, formats['header'])
    keys = [h[2] for h in columns]
    for y, d in enumerate(data.items(), start=1):
        name, values = d
        row_data = []
        for key in keys:
            if key is None:
                row_data.append(name)
            else:
                row_data.append(_get_value(values, key))
        format_name = f"element_{['even', 'odd'][y % 2]}"
        worksheet.write_row(y, 0, row_data, formats[format_name])
        _write_glossary(worksheet, y, row_data)


def _setup_columns(worksheet: Worksheet, columns, formatting):
    """Use the columns data to set up the width and headers of the columns."""
    for x, col in enumerate(columns):
        worksheet.set_column(x, x, col[1])
    headers = [col[0] for col in columns]
    worksheet.write_row(0, 0, headers, formatting)


def _get_value(data, key) -> str:
    """Get the formatted value, ready to be stored in the workbook."""
    if key in data:
        return ', '.join(data[key])
    return ''


def _write_glossary(worksheet, row_id: int, row_data: List[str]):
    """Write the comments from the glossary."""
    for x, value in enumerate(row_data):
        comment = Glossary.get(value)
        if comment is not None:
            worksheet.write_comment(row_id, x, comment)


class Glossary:
    _glossary: Dict[str, str] = None

    @classmethod
    def load(cls, filename: str):
        cls._glossary = toml.load(filename)

    @classmethod
    def set(cls, data: dict):
        cls._glossary = data

    @classmethod
    def get(cls, item: str) -> Optional[str]:
        if cls._glossary is None:
            return None
        return cls._glossary.get(item)

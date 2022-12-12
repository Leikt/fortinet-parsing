import json
from functools import reduce
from os import PathLike
from typing import Union, Any, Dict

import xlsxwriter
from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

import toml


def load_config(filename: Union[str, PathLike]) -> dict:
    """Load the given toml file."""
    with open(filename, 'r') as file:
        config = toml.loads(file.read())
    return config


def select_data(selector, selector_args, data):
    """Get the selector and raise an exception if it is invalid."""
    if selector not in SELECTORS:
        raise Exception(f"Invalid selector {selector}. Choose between {list(SELECTORS.keys())}")
    return SELECTORS[selector](data, selector_args)


def selector_path(data, path) -> Any:
    """Select data in the dictionary using a path of key."""
    res = reduce(
        lambda di, key: di.get(key, {}) if di and isinstance(di, dict) else None,
        path,
        data
    )
    return res


SELECTORS = {
    'path': selector_path
}


def generate(data: dict, config: dict):
    """Main generation function."""
    workbook = xlsxwriter.Workbook(config["general"]["destination"])
    formats = _setup_formats(workbook, config.get("formats", {}))
    for ws in config["sheet"]:
        name = ws['name']
        selector = ws['selector']
        selector_args = ws['selector_arguments']
        columns = _build_columns(ws['column'])
        _create_worksheet(select_data(selector, selector_args, data), workbook, formats, name, columns)
    workbook.close()


def _build_columns(columns_config: list) -> list:
    return [(col['name'], col['width'], col.get('source', None)) for col in columns_config]


def _get_value(data, key) -> str:
    if key in data:
        return ', '.join(data[key])
    return ''


def _setup_columns(worksheet: Worksheet, columns, formatting):
    for x, col in enumerate(columns):
        worksheet.set_column(x, x, col[1])
    headers = [col[0] for col in columns]
    worksheet.write_row(0, 0, headers, formatting)


def _create_worksheet(data, workbook, formats, sheet_name, setup):
    worksheet = workbook.add_worksheet(sheet_name)
    _setup_columns(worksheet, setup, formats['header'])
    keys = [h[2] for h in setup]
    for y, d in enumerate(data.items(), start=1):
        name, values = d
        row_data = []
        for key in keys:
            if key is None:
                row_data.append(name)
                continue

            row_data.append(_get_value(values, key))
        format_name = 'element_odd' if y % 2 == 1 else 'element_even'
        worksheet.write_row(y, 0, row_data, formats[format_name])


def _setup_formats(workbook: Workbook, formats_config: dict) -> Dict[str, Format]:
    formats = {}
    for name, properties in formats_config.items():
        formats[name] = workbook.add_format(properties)
    return formats


def main(config: Union[str, PathLike]):
    config = load_config(config)
    with open(config["general"]["source"], 'r') as file:
        data = json.load(file)
    generate(data, config)


if __name__ == "__main__":
    main("data/fortiweb_report.toml")

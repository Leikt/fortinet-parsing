# Fortiweb configuration parser and reporting

## Prerequisites

1. Install the requirements with `python -m pip install ./requirements.txt`
2. Navigate to the fortinet_reporting folder

## Parse configuration

Display help for the configuration parser

```bash
python -m fortiweb_conf_parser -h
```

To parse a config file, just run the following command:

```bash
python -m fortiweb_conf_parser path/to/config_file path/to/output/file.json
```

## Generate the report

Display the help for the xlsx generator

```bash
python -m generate_xlsx -h
```

You will need a configuration file and a data file (in json). The first one can be any json data you want and can be
obtained with the previous method.

The second one needs to be writen manually following these rules.

Once you have these two files, run the following command to generate the xlsx file :
```bash
python -m generate_xlsx path/to/data.json path/to/config.toml
```

### XLSX generation configuration

It's a toml file with the following categories

```toml
[general]
# General configuration information
destination = 'path/to/result/file.xlsx'    # The final xlsx file
source = 'path/to/data.json'                # The data used to generate the report
glossary = 'path/to/glossary.toml'          # The glossary file to use to set the comments

[formats]               # Optional
[formats.header]        # Define the format of the headers
# Use the key and valid values described here : https://xlsxwriter.readthedocs.io/format.html#format-methods-and-format-properties
[formats.element_even]  # Define the format of the elements when they are on an even row number
[formats.element_odd]   # Define the format of the elements when they are on an odd row number

[[sheet]]               # Add a new sheet to the report
name = "Sheet's name"   # Name of the sheet in the report
selector = "path"       # Name of the method used to select data. See "Selectors"
selector_arguments = [] # Arguments for the selector

[[sheet.column]]        # Add a new column to the report
name = "Header"         # Header value
width = 30              # Width of the column
source = "key"          # <Optional> Key where to search for the value in the dictionary. If omitted, the name of the dictionary will be used

[[sheet.column]]        # Add another column, you can add as many column as you want to
# ...

[[sheet]]               # Add another sheet, you can add as many sheet as you want to
```

### Selectors

Methods used to select the data rendered in a sheet.

#### path

Arguments: list of keys

Example:

```toml
selector = "path"
selector_arguments = ["france", "savoie", "chambery"]
```

This selector applied to the following dataset :

```json
{
  "usa": {
    "minesota": {
      "saint-cloud": "heillo partner"
    }
  },
  "france": {
    "ile-de-france": {
      "paris": "Bonjour"
    },
    "savoie": {
      "chambery": "Ca va ou bien?",
      "pontcharra": "???"
    }
  }
}
```

Will give "Ca va ou bien?" which is the result of the path "france" > "savoie" > "chambery"

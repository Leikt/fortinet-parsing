import xlsxwriter
from xlsxwriter.worksheet import Worksheet


def generate(data: dict, output_file: str):
    """Main generation function."""
    workbook = xlsxwriter.Workbook(output_file)
    formats = _setup_formats(workbook)
    for ws in WORKSHEETS:
        name = ws['name']
        selector = ws['selector']
        setup = ws['setup']
        _create_worksheet(selector(data), workbook, formats, name, setup)
    workbook.close()


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


def _setup_formats(workbook):
    return {
        'header': workbook.add_format(FORMAT_HEADERS),
        'element_odd': workbook.add_format(FORMAT_ELEMENT_ODD),
        'element_even': workbook.add_format(FORMAT_ELEMENT_EVEN)
    }


FORMAT_HEADERS = {"align": "center", "valign": "center", "bold": True, "bg_color": "#4287f5", "font_color": "white",
                  "text_wrap": True}
FORMAT_ELEMENT_EVEN = {"align": "center", "valign": "left", "text_wrap": True, "bg_color": "#d7e5fc"}
FORMAT_ELEMENT_ODD = {"align": "center", "valign": "left", "text_wrap": True, "bg_color": "#edf2fa"}

WS_ADDRESSES = [
    ('Name', 40, None),
    ('Type', 10, 'type'),
    ('Sub-Type', 10, 'sub-type'),
    ('Associated Interface', 15, 'associated-interface'),
    ('Start IP', 15, 'start-ip'),
    ('End IP', 15, 'end-ip'),
    ('Subnet', 30, 'subnet'),
    ('FQDN', 30, 'fqdn'),
    ('Comment', 60, 'comment')
]

WS_POLICIES = [
    ('Id', 5, None),
    ('Name', 40, 'name'),
    ('Infra source', 15, 'srcintf'),
    ('Infra destination', 15, 'dstintf'),
    ('Source Addresses', 60, 'srcaddr'),
    ('Destination Addresses', 60, 'dstaddr'),
    ('Action', 10, 'action'),
    ('Schedule', 10, 'schedule'),
    ('Service', 30, 'service'),
    ('Log Traffic', 10, 'logtraffic'),
    ('NAT', 10, 'nat'),
    ('UTM Status', 15, 'utm-status'),
    ('Webfilter Profile', 15, 'webfilter-profile'),
    ('Send Deny Packet', 15, 'send-deny-packet'),
    ('SSL SSH Profile', 20, 'ssl-ssh-profile'),
    ('IPS Sensor', 15, 'ips-sensor'),
    ('Application list', 15, 'application-list'),
    ('IP Pool', 15, 'ippool'),
    ('Pool Name', 15, 'poolname'),
    ('Status', 15, 'status'),
    ('Inspection Mode', 15, 'inspection-mode'),
    ('Comment', 60, 'comments')
]

WS_SERVICE_CATEGORIES = [
    ('Name', 30, None),
    ('Description', 60, 'comment')
]

WS_SERVICES = [
    ('Name', 25, None),
    ('Category', 25, 'category'),
    ('TCP Portrange', 20, 'tcp-portrange'),
    ('UDP Portrange', 20, 'udp-portrange'),
    ('Protocol', 10, 'protocol'),
    ('Proxy', 10, 'proxy'),
    ('ICMP Type', 10, 'icmptype')
]

WS_SERVICES_GROUPS = [
    ('Name', 30, None),
    ('Members', 60, 'member')
]

WS_VIP = [
    ('URL', 40, None),
    ('Ext IP', 20, 'extip'),
    ('Mapped IP', 20, 'mappedip'),
    ('Ext Intf', 10, 'extintf'),
    ('Comment', 60, 'comment')
]

WORKSHEETS = [
    {
        'name': 'Addresses',
        'setup': WS_ADDRESSES,
        'selector': lambda d: d['firewall']['address']
    },
    {
        'name': 'Policies',
        'setup': WS_POLICIES,
        'selector': lambda d: d['firewall']['policy']
    },
    {
        'name': 'Service Categories',
        'setup': WS_SERVICE_CATEGORIES,
        'selector': lambda d: d['firewall']['service']['category']
    },
    {
        'name': 'Services',
        'setup': WS_SERVICES,
        'selector': lambda d: d['firewall']['service']['custom']
    },
    {
        'name': 'Services Groups',
        'setup': WS_SERVICES_GROUPS,
        'selector': lambda d: d['firewall']['service']['group']
    },
    {
        'name': 'VIP',
        'setup': WS_VIP,
        'selector': lambda d: d['firewall']['vip']
    }
]

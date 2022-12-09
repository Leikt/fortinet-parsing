import unittest

from fortinet_reporter.parser import parse
from fortinet_reporter.stream_handler import StreamHandler


class TestParser(unittest.TestCase):
    def test_basic(self):
        config = """config test a
    set param1 value
end"""
        stream = StreamHandler(config)
        actual = parse(stream)
        expected = [{
            'type': 'config',
            'parameters': ['test', 'a'],
            'data': [
                {
                    'type': 'set',
                    'name': 'param1',
                    'parameters': ['value']
                }
            ]
        }]
        self.assertEqual(expected, actual)

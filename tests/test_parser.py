import unittest

from fortiweb_conf_parser.parser import parse_set, parse_unset, parse_block
from fortiweb_conf_parser.stream_handler import StreamHandler


class TestParser(unittest.TestCase):
    def test_set(self):
        code = "set param1 value\nset param2 value1 value2 value3"
        stream = StreamHandler(code)
        context = {}
        stream.next()

        parse_set(context, stream)
        stream.next()
        parse_set(context, stream)
        self.assertEqual({
            'param1': ['value'],
            'param2': ['value1', 'value2', 'value3']
        }, context)

    def test_unset(self):
        code = "set param1 value\nunset param1"
        stream = StreamHandler(code)
        context = {}
        stream.next()

        parse_set(context, stream)
        stream.next()
        parse_unset(context, stream)
        self.assertEqual({}, context)

    def test_config(self):
        code = "config c1 glob\n\tset p1 v1\nend"
        stream = StreamHandler(code)
        context = {}
        stream.next()

        parse_block(context, stream, 'end')
        self.assertEqual({
            'c1': {
                'glob': {
                    'p1': ['v1']
                }
            }
        }, context)
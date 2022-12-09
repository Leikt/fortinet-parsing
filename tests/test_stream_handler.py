import unittest

from stream_handler import StreamHandler


class TestStreamHandler(unittest.TestCase):
    def test_basic_stream(self):
        src_code = "test a b c"
        stream = StreamHandler(src_code)
        self.assertEqual('test', stream.get_next())
        self.assertEqual('a', stream.get_next())
        self.assertEqual('b', stream.get_next())
        self.assertEqual('c', stream.get_next())

    def test_new_line(self):
        src_code = """test a
b
c"""
        stream = StreamHandler(src_code)
        self.assertEqual('test', stream.get_next())
        self.assertEqual('a', stream.get_next())
        stream.next()
        self.assertTrue(stream.is_new_line())
        self.assertEqual('b', stream.get_next())
        stream.next()
        self.assertTrue(stream.is_new_line())
        self.assertEqual('c', stream.get_next())

    def test_choices(self):
        src_code = "ka"
        stream = StreamHandler(src_code)
        stream.next()
        self.assertEqual('ka', stream.token_choices(['ka', 'kb']))

    def test_choices_exception(self):
        stream = StreamHandler("ka")
        stream.next()
        with self.assertRaises(ValueError):
            stream.token_choices(['valid_kw'])

    def test_token_casting(self):
        stream = StreamHandler('some_string 12 15.0')
        self.assertIsInstance(stream.get_next(), str)
        self.assertIsInstance(stream.get_next(int), int)
        self.assertIsInstance(stream.get_next(float), float)

    def test_custom_token_casting(self):
        def cast_boolean(s: str) -> bool:
            if s.lower() in ['yes', 'y', 'true']:
                return True
            elif s.lower() in ['no', 'n', 'false']:
                return False
            raise ValueError(f"Not a valid boolean string: {s}")

        stream = StreamHandler('yes no true false not_a_boolean')
        self.assertTrue(stream.get_next(cast_boolean))
        self.assertFalse(stream.get_next(cast_boolean))
        self.assertTrue(stream.get_next(cast_boolean))
        self.assertFalse(stream.get_next(cast_boolean))
        with self.assertRaises(ValueError):
            stream.get_next(cast_boolean)

    def test_token_casting_exception(self):
        stream = StreamHandler('not_an_int')
        with self.assertRaises(ValueError):
            stream.get_next(int)
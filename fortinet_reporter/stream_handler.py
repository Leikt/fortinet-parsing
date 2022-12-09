import shlex
from typing import TypeVar, List

T = TypeVar('T')

NEW_LINE = '___new_line___'


class StreamHandler:
    """Handle the stream of tokens in the configuration file

    **Usage**
    stream_handler = StreamHandler("path/to/configuration_file")
    while stream_handler.next():
        current_token = stream_handler.token()
        current_int_token = stream_handler.token(int)
    """

    def __init__(self, source_code: str):
        lines = source_code.splitlines()
        lines = [line.strip() for line in lines]
        mono_line = f' {NEW_LINE} '.join(lines)
        self._data = shlex.split(mono_line)
        self._index = -1
        self._token = None
        self._len = len(self._data)
        self._line_number = 1

    def next(self) -> bool:
        """Move the stream to the next token."""
        if self.is_new_line():
            self._line_number += 1
        self._index += 1
        if self._index >= self._len:
            self._token = None
            return False
        self._token = self._data[self._index]
        return True

    def get_next(self, t: T = str) -> T:
        """Get the next token"""
        self.next()
        return self.token(t)

    def token(self, t: T = str) -> T:
        """Get the token and convert it to the given type."""
        try:
            return t(self._token)
        except ValueError:
            raise ValueError(f"(Line {self._line_number}) Expect token of type '{t}' but got '{self._token}' ({type(self._token)})")

    def is_new_line(self) -> bool:
        """Check if the token is a new line."""
        return self._token == NEW_LINE

    def skip_comments(self):
        """Skip every token to the next not commented line if the current token is a comment."""
        if not self._token or not self._token.startswith('#'):
            return
        while self._token and self._token.startswith('#'):
            while not self.is_new_line() and self.next():
                pass
            self.next()

    def token_choices(self, choices: List[T], t: T = str) -> T:
        """Check if the current token is one of these choices and returns it."""
        token = self.token(t)
        if token not in choices:
            raise ValueError(f"(Line {self._line_number}) Expect one of {choices} but got '{token}'.")
        return token

    def tokens_to_eol(self) -> List[str]:
        """Gather all the tokens to the end of the line. Tokens will be strings."""
        tokens = []
        while self.next() and not self.is_new_line():
            tokens.append(self.token())
        return tokens

    def expect_eol(self):
        if self.is_new_line() or self._token is None:
            return
        raise SyntaxError("(Line {self._line_number}) Expect new line.")

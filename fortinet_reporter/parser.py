from functools import partial
from typing import Any

from .stream_handler import StreamHandler


def parse(stream: StreamHandler) -> Any:
    context = {}
    while stream.next():
        stream.skip_comments()
        keyword = stream.token_choices(KEYWORDS)
        SUB_PARSERS[keyword](context, stream)
    return context


def parse_set(context: dict, stream: StreamHandler) -> None:
    name = stream.get_next()
    values = stream.tokens_to_eol()
    context[name] = values


def parse_unset(context: dict, stream: StreamHandler) -> None:
    names = stream.tokens_to_eol()
    for name in names:
        if name in context:
            del context[name]


def parse_block(context: dict, stream: StreamHandler, end_keyword: str) -> None:
    path = stream.tokens_to_eol()
    for key in path:
        context[key] = context.get(key, dict())
        context = context[key]
    stream.expect_eol()

    while stream.next():
        stream.skip_comments()
        if stream.token() == end_keyword:
            break

        keyword = stream.token_choices(KEYWORDS)
        SUB_PARSERS[keyword](context, stream)
    stream.next()  # skip end keyword


SUB_PARSERS = {
    'set': parse_set,
    'unset': parse_unset,
    'config': partial(parse_block, end_keyword='end'),
    'edit': partial(parse_block, end_keyword='next')
}
KEYWORDS = list(SUB_PARSERS.keys())

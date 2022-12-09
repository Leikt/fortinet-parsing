from functools import partial

from .stream_handler import StreamHandler


def parse(stream: StreamHandler) -> dict:
    """Main parsing function. Give it the stream and get the parsed configuration in output."""
    context = {}
    while stream.next():
        stream.skip_comments()
        keyword = stream.token_choices(KEYWORDS)
        SUB_PARSERS[keyword](context, stream)
    return context


def parse_set(context: dict, stream: StreamHandler) -> None:
    """Parses the 'set' keyword."""
    name = stream.get_next()
    values = stream.tokens_to_eol()
    context[name] = values


def parse_unset(context: dict, stream: StreamHandler) -> None:
    """Parses the 'unset' keyword."""
    names = stream.tokens_to_eol()
    for name in names:
        if name in context:
            del context[name]


def parse_block(context: dict, stream: StreamHandler, end_keyword: str) -> None:
    """Parses a block and its content into sub contexts."""
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

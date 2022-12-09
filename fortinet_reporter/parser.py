from typing import Any, Callable, Dict

from .stream_handler import StreamHandler


def parse(stream: StreamHandler) -> Any:
    data = []
    while stream.next():
        stream.skip_comments()
        keyword = stream.token_choices(KEYWORDS)
        subparser: Parser = SUBPARSERS[keyword]
        data.append(subparser(stream))
    return data


def parse_config(stream: StreamHandler) -> Any:
    data = {
        'type': 'config',
        'parameters': stream.tokens_to_eol(),
        'data': []
    }
    stream.expect_eol()
    while stream.next():
        if stream.token() == 'end':
            break
        stream.skip_comments()
        keyword = stream.token_choices(KEYWORDS)
        subparser: Parser = SUBPARSERS[keyword]
        data['data'].append(subparser(stream))
    stream.next()
    stream.expect_eol()
    return data


def parse_edit(stream: StreamHandler) -> Any:
    data = {
        'type': 'edit',
        'name': stream.get_next(),
        'data': []
    }
    stream.next()
    stream.expect_eol()
    while stream.next():
        if stream.token() == 'next':
            break
        stream.skip_comments()
        keyword = stream.token_choices(KEYWORDS)
        subparser: Parser = SUBPARSERS[keyword]
        data['data'].append(subparser(stream))
    stream.next()
    stream.expect_eol()
    return data


def parse_set(stream: StreamHandler) -> Any:
    return {
        'type': 'set',
        'name': stream.get_next(),
        'parameters': stream.tokens_to_eol()
    }


def parse_unset(stream: StreamHandler) -> Any:
    data = {
        'type': 'unset',
        'name': stream.get_next()
    }
    stream.next()
    stream.expect_eol()
    return data


Parser = Callable[[StreamHandler], Any]

SUBPARSERS: Dict[str, Parser] = {
    'config': parse_config,
    'edit': parse_edit,
    'set': parse_set,
    'unset': parse_unset
}
KEYWORDS = list(SUBPARSERS.keys())

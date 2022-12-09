from typing import Any, Callable, Dict

from .stream_handler import StreamHandler


def parse(stream: StreamHandler) -> Any:
    data = []
    while stream.next():
        stream.skip_comments()
        keyword = stream.token_choices(KEYWORDS)
        subparser: Parser = SUBPARSERS[keyword]
        data.append(subparser(keyword, stream))
    return data


def parse_block(keyword: str, stream: StreamHandler) -> Any:
    data = {
        'type': keyword,
        'parameters': stream.tokens_to_eol(),
        'data': []
    }
    stream.expect_eol()
    while stream.next():
        if stream.token() == BLOCKEND_KEYWORDS[keyword]:
            break
        stream.skip_comments()
        sub_keyword = stream.token_choices(KEYWORDS)
        subparser: Parser = SUBPARSERS[sub_keyword]
        data['data'].append(subparser(sub_keyword, stream))
    stream.next()
    stream.expect_eol()
    return data


def parse_line(keyword: str, stream: StreamHandler) -> Any:
    return {
        'type': keyword,
        'name': stream.get_next(),
        'parameters': stream.tokens_to_eol()
    }


Parser = Callable[[str, StreamHandler], Any]

SUBPARSERS: Dict[str, Parser] = {
    'config': parse_block,
    'edit': parse_block,
    'set': parse_line,
    'unset': parse_line
}
KEYWORDS = list(SUBPARSERS.keys())
BLOCKEND_KEYWORDS = {
    'config': 'end',
    'edit': 'next'
}

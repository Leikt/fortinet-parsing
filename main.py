from fortinet_reporter.stream_handler import StreamHandler

stream = StreamHandler('data/C8ASPFIRACC.conf')

while stream.next():
    # stream.next()
    stream.skip_comments()
    token = stream.token_choices(['config', 'set', 'edit', 'unset', 'end', 'next'])
    parameters = stream.tokens_to_eol()
    print(token, parameters)

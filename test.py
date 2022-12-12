from functools import reduce

d = {'a': {'b': {'c': {"value": "ll"}}, 'e': 'aaaa'}}
v = reduce(lambda di, key: di.get(key, {}) if di and isinstance(di, dict) else None, ['a', 'b'], d)
print(v)
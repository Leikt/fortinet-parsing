from typing import Any, List


def select_data(selector: str, selector_args: Any, data: dict):
    """Select the data in the given dict."""
    if selector not in _SELECTORS:
        raise Exception(f"Invalid selector {selector}. Choose between {list(_SELECTORS.keys())}")
    return _SELECTORS[selector](data, selector_args)


def _selector_path(data: dict, path: List[str]) -> Any:
    """Select data in the dictionary using a path of key."""
    res = data
    for p in path:
        res = res[p]
    return res


_SELECTORS = {
    'path': _selector_path
}

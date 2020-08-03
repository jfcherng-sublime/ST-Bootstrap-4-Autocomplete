import sublime

from functools import lru_cache
from typing import List


def get_package_name() -> str:
    """
    Gets the package name.

    :returns: The package name.
    :rtype:   str
    """

    return __package__.partition(".")[0]


DATA_FILE = "Packages/%s/data.json" % get_package_name()


@lru_cache
def get_completion_items() -> List[sublime.CompletionItem]:
    """
    Gets the completion items.

    :returns: The completion items.
    :rtype:   List[sublime.CompletionItem]
    """

    return list(
        map(
            lambda item: sublime.CompletionItem(
                trigger=item[0],
                annotation="Bootstrap 4 Class",
                completion=item[0],
                completion_format=sublime.COMPLETION_FORMAT_TEXT,
                kind=(sublime.KIND_ID_MARKUP, "c", ""),
                details="",
            ),
            sublime.decode_value(sublime.load_resource(DATA_FILE)),
        ),
    )

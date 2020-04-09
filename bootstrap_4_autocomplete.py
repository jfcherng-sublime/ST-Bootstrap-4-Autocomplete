from .functions import get_completion_items
import sublime
import sublime_plugin

COMPLETION_ITEMS = []


def plugin_loaded() -> None:
    global COMPLETION_ITEMS

    COMPLETION_ITEMS = get_completion_items()


class Bootstrap4Completions(sublime_plugin.EventListener):
    def __init__(self):
        self.working_scopes = ["meta.attribute-with-value.class.html"]

    def on_query_completions(self, view, prefix, locations) -> list:
        point = locations[0]

        if view.match_selector(point, "|".join(self.working_scopes)):
            return COMPLETION_ITEMS

        if view.match_selector(point, "text.html string.quoted"):
            LIMIT = 250
            cursor = point - len(prefix) - 1
            start = max(0, cursor - LIMIT - len(prefix))
            line = view.substr(sublime.Region(start, cursor))
            parts = line.split("=")

            if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return COMPLETION_ITEMS

        return []

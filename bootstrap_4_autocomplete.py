import sublime
import sublime_plugin

from typing import List

from .functions import get_completion_items


class Bootstrap4Completions(sublime_plugin.EventListener):
    working_scopes = ["meta.attribute-with-value.class.html"]

    def on_query_completions(
        self, view: sublime.View, prefix: str, locations: List[int]
    ) -> List[sublime.CompletionItem]:
        point = locations[0]

        if view.match_selector(point, "|".join(self.working_scopes)):
            return get_completion_items()

        if view.match_selector(point, "text.html string.quoted"):
            LIMIT = 250
            cursor = point - len(prefix) - 1
            start = max(0, cursor - LIMIT - len(prefix))
            line = view.substr(sublime.Region(start, cursor))
            parts = line.split("=")

            if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return get_completion_items()

        return []

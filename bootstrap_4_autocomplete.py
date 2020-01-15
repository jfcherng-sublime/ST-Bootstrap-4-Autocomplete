from .bootstrap_4_data import classes as bs4_classes
import sublime
import sublime_plugin


class Bootstrap4Completions(sublime_plugin.EventListener):
    def __init__(self):
        if int(sublime.version()) < 4000:
            self.class_completions = [("%s\tBootstrap 4 Class" % s, s) for s in bs4_classes]
        else:
            self.class_completions = list(
                map(
                    lambda bs4_class: sublime.CompletionItem(
                        trigger=bs4_class,
                        annotation="Bootstrap 4 Class",
                        completion=bs4_class,
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=sublime.KIND_MARKUP,
                    ),
                    bs4_classes,
                )
            )

        self.working_scopes = ["meta.attribute-with-value.class.html"]

    def on_query_completions(self, view, prefix, locations):
        point = locations[0]

        if view.match_selector(point, "|".join(self.working_scopes)):
            return self.class_completions

        if view.match_selector(point, "text.html string.quoted"):
            LIMIT = 250
            cursor = point - len(prefix) - 1
            start = max(0, cursor - LIMIT - len(prefix))
            line = view.substr(sublime.Region(start, cursor))
            parts = line.split("=")

            if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return self.class_completions

        return []

import sublime
import sublime_plugin

IS_ST4 = int(sublime.version()) >= 4000
DATA_FILE = "Packages/%s/data.json" % __package__


class Bootstrap4Completions(sublime_plugin.EventListener):
    def __init__(self):
        self.completion_items = self.get_completion_items()
        self.working_scopes = ["meta.attribute-with-value.class.html"]

    def on_query_completions(self, view, prefix, locations) -> list:
        point = locations[0]

        if view.match_selector(point, "|".join(self.working_scopes)):
            return self.completion_items

        if view.match_selector(point, "text.html string.quoted"):
            LIMIT = 250
            cursor = point - len(prefix) - 1
            start = max(0, cursor - LIMIT - len(prefix))
            line = view.substr(sublime.Region(start, cursor))
            parts = line.split("=")

            if len(parts) > 1 and parts[-2].strip().endswith("class"):
                return self.completion_items

        return []

    @staticmethod
    def get_completion_items() -> list:
        data = sublime.decode_value(sublime.load_resource(DATA_FILE))
        annotation = "Bootstrap 4 Class"

        if IS_ST4:
            completions = list(
                map(
                    lambda item: sublime.CompletionItem(
                        trigger=item[0],
                        annotation=annotation,
                        completion=item[0],
                        completion_format=sublime.COMPLETION_FORMAT_TEXT,
                        kind=(sublime.KIND_ID_MARKUP, "c", ""),
                        details="",
                    ),
                    data,
                ),
            )
        else:
            completions = [("%s\t%s" % (item[0], annotation)) for item in data]

        return completions

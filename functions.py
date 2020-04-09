import sublime

IS_ST4 = int(sublime.version()) >= 4000


def get_package_name() -> str:
    return __package__.partition(".")[0]


DATA_FILE = "Packages/%s/data.json" % get_package_name()


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

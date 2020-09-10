import os

from isort import code, settings
from pyls import hookimpl


def sort(document, override=None):
    source = override or document.source
    isort_config = settings.Config(settings_path=os.path.dirname(document.path))
    sorted_source = code(source, config=isort_config)
    if source == sorted_source:
        return
    change_range = {
        "start": {"line": 0, "character": 0},
        "end": {"line": len(document.lines), "character": 0},
    }
    return [{"range": change_range, "newText": sorted_source}]


@hookimpl(hookwrapper=True)
def pyls_format_document(document):
    outcome = yield
    results = outcome.get_result()
    if results:
        newResults = sort(document, results[0]["newText"])
    else:
        newResults = sort(document)

    if newResults:
        outcome.force_result(newResults)


@hookimpl(hookwrapper=True)
def pyls_format_range(document, range):
    outcome = yield
    results = outcome.get_result()
    if results:
        newResults = sort(document, results[0]["newText"])
    else:
        newResults = sort(document)

    if newResults:
        outcome.force_result(newResults)

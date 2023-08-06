import copy

from deepdiff import DeepDiff
from nested_lookup import nested_delete

from response_differ import play, get_grouped_exception


def check_status_code(replayed):
    if not replayed.response.ok:
        message = f"URL:{replayed.response.url}\n " \
                  f"STATUS CODE: {replayed.response.status_code}"
        play.Replayed.errors.append(AssertionError(message))


def check_diff_responses():
    for i in play.Replayed.responses:
        if i['uri'] in play.Replayed.config:
            old = i['old']
            new = i['new']
            if play.Replayed.config[i['uri']]:
                old = _filter(old, filters=play.Replayed.config[i['uri']])
                new = _filter(new, filters=play.Replayed.config[i['uri']])
            result = DeepDiff(old, new, ignore_order=True)
            print(result)
            if result.get('values_changed'):
                message = f"ERROR {result}"
                play.Replayed.errors.append(AssertionError(message))
                exception_cls = get_grouped_exception(*play.Replayed.errors)
                raise exception_cls(play.Replayed.errors)


def _filter(resp, filters):
    filtered_resp = copy.deepcopy(resp)
    for f in filters:
        filtered_resp = _filter(nested_delete(filtered_resp, f), filters=filters[1::])
    return filtered_resp

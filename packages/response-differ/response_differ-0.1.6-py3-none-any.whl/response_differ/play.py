import json
from os.path import dirname
from urllib.parse import urlparse

import requests
import attr
import yaml
from requests.cookies import RequestsCookieJar
from requests.structures import CaseInsensitiveDict

from response_differ import cheks
from response_differ.cassettes import filter_cassette, d_vcr


@attr.s(slots=True)
class Replayed:
    interaction = attr.ib()
    response = attr.ib()
    responses = []
    config = attr.ib(default={})
    errors = []


def get_prepared_request(data):
    prepared = requests.PreparedRequest()
    prepared.method = data["method"]
    prepared.url = data["uri"]
    prepared._cookies = RequestsCookieJar()
    prepared.body = data["body"]
    prepared.headers = [{'Content-Length': ['20']}]
    if data.get('headers'):
        prepared.headers = CaseInsensitiveDict([(key, value[0]) for key, value in data["headers"].items()])
    return prepared


def store_responses(replayed):
    if not replayed.interaction.get('response'):
        raise Exception("Not response. не передавайте флаг дифф")
    Replayed.responses.append(
        {
            'uri': urlparse(replayed.interaction['request']['uri']).path,
            'old': json.loads(replayed.interaction['response']['body']['string']),
            'new': replayed.response.json()
        })


def replay(cassette, cassette_path, status=None, uri=None, diff=None):
    session = requests.Session()
    for interaction in filter_cassette(cassette["interactions"], status, uri):
        request = get_prepared_request(interaction["request"])
        with d_vcr.use_cassette(f'new_{cassette_path}'):
            response = session.send(request)
            replayed = Replayed(interaction, response)
            yield replayed
            cheks.check_status_code(replayed)
            diff and store_responses(replayed)


def reed_conf(path):
    project_root = dirname(dirname(__file__))
    with open(f'{project_root}/{path}') as fd:
        cassette = yaml.load(fd, Loader=yaml.SafeLoader)
    return cassette

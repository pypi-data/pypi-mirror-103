import json
from urllib.parse import urlparse

import requests
import attr
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
    prepared.headers = CaseInsensitiveDict([('Accept', '*/*')])
    if data.get('headers'):
        prepared.headers = CaseInsensitiveDict([(key, value[0]) for key, value in data["headers"].items()])
    #if data.get('headers'):
    #    prepared.headers = CaseInsensitiveDict(data["headers"])
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
    #session = requests.Session()
    for interaction in filter_cassette(cassette["interactions"], status, uri):
        request = interaction["request"]
        if not request.get('headers'):
           request['headers'] = {}
        else:
            request['headers'] = CaseInsensitiveDict([(key, value[0]) for key, value in request["headers"].items()])
        #request = get_prepared_request(interaction["request"])
        with d_vcr.use_cassette(f'new_{cassette_path}'):
            response = requests.post(request['uri'], headers=request['headers'], data=request['body'])
            #response = session.send(request)
            replayed = Replayed(interaction, response)
            yield replayed
            cheks.check_status_code(replayed)
            diff and store_responses(replayed)

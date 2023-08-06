import os
import re

import yaml
from vcr import VCR
from vcr.request import Request
from vcr.serialize import CASSETTE_FORMAT_VERSION, _warn_about_old_cassette_format, _looks_like_an_old_cassette
from vcr.serializers import compat

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


class BinarySerializer(object):

    @classmethod
    def deserialize(cls, cassette_string):
        try:
            data = yaml.load(cassette_string, Loader=Loader)
        except (ImportError, yaml.constructor.ConstructorError):
            _warn_about_old_cassette_format()
        if _looks_like_an_old_cassette(data):
            _warn_about_old_cassette_format()

        requests = [Request._from_dict(r["request"]) for r in data["interactions"]]
        responses = [compat.convert_to_bytes(r["response"]) for r in data["interactions"] if r.get('response')]
        return requests, responses

    @classmethod
    def serialize(cls, cassette_dict):
        interactions = [
            {
                "id": str(i),
                "request": compat.convert_to_unicode(r[0]._to_dict()),
                "response": compat.convert_to_unicode(r[1]),
            }
            for i, r in enumerate(zip(cassette_dict["requests"], cassette_dict["responses"]))
        ]
        data = {"version": CASSETTE_FORMAT_VERSION, "interactions": interactions}
        return yaml.dump(data, Dumper=Dumper)


class CustomPersister:
    @classmethod
    def load_cassette(cls, cassette_path, serializer=BinarySerializer):
        try:
            with open(cassette_path) as f:
                cassette_content = f.read()
        except OSError:
            raise ValueError("Cassette not found.")
        cassette = serializer.deserialize(cassette_content)
        return cassette

    @staticmethod
    def save_cassette(cassette_path, cassette_dict,
                      serializer=BinarySerializer):
        data = serializer.serialize(cassette_dict)
        dirname, filename = os.path.split(cassette_path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        with open(cassette_path, "wb") as f:
            f.write(data.encode('utf-8'))


def filter_cassette(
        interactions, id_=None, status=None, uri=None, method=None
):

    filters = []

    def id_filter(item):
        return item["id"] == id_

    def status_filter(item):
        return item["status"].upper() == status.upper()

    def uri_filter(item):
        return bool(re.search(uri, item["request"]["uri"]))

    def method_filter(item):
        return bool(re.search(method, item["request"]["method"]))

    if id_ is not None:
        filters.append(id_filter)

    if status is not None:
        filters.append(status_filter)

    if uri is not None:
        filters.append(uri_filter)

    if method is not None:
        filters.append(method_filter)

    def is_match(interaction):
        return all(filter_(interaction) for filter_ in filters)

    return filter(is_match, interactions)


d_vcr = VCR(record_mode='new_episodes')
d_vcr.register_serializer(name='binary', serializer=BinarySerializer())
d_vcr.serializer = 'binary'
d_vcr.register_persister(CustomPersister)

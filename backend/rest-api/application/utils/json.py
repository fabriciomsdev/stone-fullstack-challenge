import falcon
from utils.json import ComplexObjectToJsonEntityMixin
import json

def serialize(obj: object):
    if isinstance(obj, dict):
        return falcon.media.JSONHandler().serialize(obj, falcon.MEDIA_JSON)
    else:
        return falcon.media.JSONHandler().serialize(obj.__dict__, falcon.MEDIA_JSON)

def deserialize(obj: object):
    return falcon.media.JSONHandler().deserialize(obj.__dict__, falcon.MEDIA_JSON, len(obj.__dict__))


def obj_to_dict(obj: object):
    if isinstance(obj, ComplexObjectToJsonEntityMixin):
        return obj.to_dict()
    elif isinstance(obj, dict):
        return obj
    else:
        return obj.__dict__

def prepare_list_to_json(item_list: list) -> list:
    return [ obj_to_dict(item) for item in item_list ]

def deprepare_list_to_json(item_list: list) -> list:
    return [ deserialize(item) for item in item_list ]

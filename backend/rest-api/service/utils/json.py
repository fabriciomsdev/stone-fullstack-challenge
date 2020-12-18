import falcon
from utils.json import ComplexObjectToJsonEntityMixin

def serialize(obj: object):
    if isinstance(obj, dict):
        return falcon.media.JSONHandler().serialize(obj, falcon.MEDIA_JSON)
    else:
        return falcon.media.JSONHandler().serialize(obj.__dict__, falcon.MEDIA_JSON)

def deserialize(obj: object):
    return falcon.media.JSONHandler().deserialize(obj.__dict__, falcon.MEDIA_JSON, len(obj.__dict__))

def serialize_list(item_list: list) -> list:
    return [ serialize(item) for item in item_list ]

def deserialize_list(item_list: list) -> list:
    return [ deserialize(item) for item in item_list ]

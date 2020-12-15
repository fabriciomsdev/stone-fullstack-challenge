import falcon

def serialize(obj: object):
    return falcon.media.JSONHandler().serialize(obj.__dict__, falcon.MEDIA_JSON)

def deserialize(obj: object):
    return falcon.media.JSONHandler().deserialize(obj.__dict__, falcon.MEDIA_JSON, len(obj.__dict__))
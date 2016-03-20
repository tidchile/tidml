import os
from abc import ABCMeta


class Parameterized(object):
    """Abstract base class of parameterized classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self.__params = params

    @property
    def params(self):
        return self.__params


def load_config(filepath):
    config = open(filepath, 'r').read()
    ext = os.path.splitext(filepath)[1]
    if ext == '.yaml':
        import yaml
        return yaml.load(config)
    elif ext == '.json':
        import json
        return json.loads(config)
    else:
        raise NotImplementedError('Not implemented config format ' + ext)

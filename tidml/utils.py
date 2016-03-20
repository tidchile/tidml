from abc import ABCMeta


class Parameterized(object):
    """Abstract base class of parameterized classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self.__params = params

    @property
    def params(self):
        return self.__params

from abc import ABCMeta, abstractmethod


class Preparator(object):
    """Abstract base class of preparator classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self._params = params

    @property
    def params(self):
        return self._params

    @abstractmethod
    def prepare(self, data):
        """

        :param data: Training data.
        :return: Prepared data.
        """
        pass


class IdentityPreparator(Preparator):
    """
    Return training data without any special preparation.
    """

    def prepare(self, data):
        return data

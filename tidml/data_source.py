from abc import ABCMeta, abstractmethod


class DataSource(object):
    """Abstract base class of data source classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self._params = params

    @property
    def params(self):
        return self._params

    @abstractmethod
    def read_training(self):
        """

        :return: Training data.
        """
        pass

    def read_eval(self):
        """

        Optional override.

        :return: Eval data.
        """
        pass

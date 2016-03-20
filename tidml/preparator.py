from abc import ABCMeta, abstractmethod
from tidml.utils import Parameterized


class Preparator(Parameterized):
    """Abstract base class of preparator classes."""

    __metaclass__ = ABCMeta

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

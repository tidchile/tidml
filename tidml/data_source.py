from abc import ABCMeta, abstractmethod
from tidml.utils import Parameterized


class DataSource(Parameterized):
    """Abstract base class of data source classes."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def read_training(self):
        """

        :return: Training data.
        """

    def read_eval(self):
        """

        Optional override.

        :return: Eval data.
        """

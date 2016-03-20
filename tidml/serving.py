from abc import ABCMeta, abstractmethod
from tidml.utils import Parameterized


class Serving(Parameterized):
    """Abstract base class of serving classes."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def serve(self, query, results):
        """Post-process and/or combine results from different algorithms.

        :param query: Query.
        :param results: Results dictionary.
        :return: Final result.
        """
        pass


class FirstServing(Serving):
    """Serve just the first result."""

    def serve(self, query, results):
        return results.values()[0]


class AverageServing(Serving):
    """Calculate the average of a list of results."""

    def serve(self, query, results):
        values = results.values()
        return sum(values) / float(len(values))

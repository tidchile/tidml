from abc import ABCMeta, abstractmethod


class Serving(object):
    """Abstract base class of serving classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self._params = params

    @property
    def params(self):
        return self._params

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

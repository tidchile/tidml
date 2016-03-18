from abc import ABCMeta, abstractmethod
from tidml.model_persistor import PickleModelPersistor


class Algorithm(object):
    """Abstract base class of algorithm classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params={}):
        self._params = params

    @property
    def params(self):
        return self._params

    @abstractmethod
    def train(self, data):
        """Build a model using training data.

        :param data: Training data.
        :return: Model.
        """
        pass

    @abstractmethod
    def predict(self, model, query):
        """Predict a result using a model and a query.

        :param model: Model.
        :param query: Query.
        :return: Predicted result.
        """
        pass

    @property
    def persistor(self):
        """Return a model persistor instance.

        :return: Model persistor instance.
        """
        return PickleModelPersistor({
            'model.pickle': self._params['model.pickle']
        })

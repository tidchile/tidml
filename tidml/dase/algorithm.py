from abc import ABCMeta, abstractmethod
from tidml.dase.model_persistor import PickleModelPersistor
from tidml.utils import Parameterized


class Algorithm(Parameterized):
    """Abstract base class of algorithm classes."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def train(self, data):
        """Build a model using training data.

        :param data: Training data.
        :return: Model.
        """

    @abstractmethod
    def predict(self, model, query):
        """Predict a result using a model and a query.

        :param model: Model.
        :param query: Query.
        :return: Predicted result.
        """

    @property
    def persistor(self):
        """Return a model persistor instance.

        :return: Model persistor instance.
        """
        return PickleModelPersistor({
            'model.pickle': self.params['model.pickle']
        })

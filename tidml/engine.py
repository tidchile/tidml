import six
from tidml.preparator import IdentityPreparator
from abc import ABCMeta, abstractmethod


class BaseEngine(object):
    """Abstract base class of engine classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params):
        self._params = params

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass


class Engine(BaseEngine):
    """Engine default implementation."""

    def train(self):
        """Train an algorithm.

        :return: Model
        """
        datasource = self._instantiate('datasource')
        preparator = self._instantiate('preparator')
        algorithm = self._instantiate('algorithm')
        training_data = datasource.read_training()
        prepared_data = preparator.prepare(training_data)
        model = algorithm.train(prepared_data)
        algorithm.persistor.save(model)

    def predict(self, query):
        """Predict a query.

        :param query: Query.
        :return: Prediction.
        """
        algorithm = self._instantiate('algorithm')
        model = algorithm.persistor.load()
        prediction = algorithm.predict(model, query)
        return prediction

    def evaluate(self, query):
        """Evaluate the algorithm.

        :return: List of evaluation info, and tuple of
                 query, predicted result, and actual result.
        """
        pass

    def _instantiate(self, name):
        """Instantiate class with params.
        """
        spec = self._params[name]
        ctor = spec['class']
        params = spec.get('params', {})

        if isinstance(ctor, six.string_types):
            import importlib
            module_name, class_name = ctor.rsplit(".", 1)
            ctor = getattr(importlib.import_module(module_name), class_name)

        instance = ctor(params)

        return instance


class SimpleEngine(Engine):
    """Engine with default simple configuration.

    - Identity preparator.
    """

    def __init__(self, params):
        super(SimpleEngine, self).__init__({
            'datasource': params['datasource'],
            'preparator': {
                'class': IdentityPreparator,
            },
            'algorithm': params['algorithm'],  # TODO: {'': params['algorithm']}
            # 'serving': tidml.FirstServing,
        })

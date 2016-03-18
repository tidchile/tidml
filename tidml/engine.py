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
        training_data = datasource.read_training()
        self._sanity_check(training_data, 'training_data')

        preparator = self._instantiate('preparator')
        prepared_data = preparator.prepare(training_data)
        self._sanity_check(prepared_data, 'prepared_data')

        algorithm = self._instantiate('algorithm')
        model = algorithm.train(prepared_data)
        self._sanity_check(model, 'model')

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
            module = importlib.import_module(module_name)
            ctor = getattr(module, class_name)

        instance = ctor(params)

        return instance

    @staticmethod
    def _sanity_check(data, label):
        # TODO: logging
        if hasattr(data, 'sanity_check'):
            data.sanity_check(label)


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

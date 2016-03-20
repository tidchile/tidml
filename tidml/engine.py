import six
from abc import ABCMeta, abstractmethod
from tidml.preparator import IdentityPreparator
from tidml.serving import FirstServing
from tidml.utils import Parameterized


class BaseEngine(Parameterized):
    """Abstract base class of engine classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params):
        super(BaseEngine, self).__init__(self._load(params))

    @abstractmethod
    def train(self):
        pass

    @abstractmethod
    def evaluate(self):
        pass

    @staticmethod
    def _load(params):
        if params.get('config'):
            filepath = params.get('config')
            config = open(filepath, 'r').read()
            import os
            ext = os.path.splitext(filepath)[1]
            if ext == '.yaml':
                import yaml
                params = yaml.load(config)
            elif ext == '.json':
                import json
                params = json.loads(config)

        if params.get('algorithm'):
            params['algorithms'] = {'': params['algorithm']}

        return params


class Engine(BaseEngine):
    """Engine default implementation."""

    def train(self):
        """Train an algorithm.

        :return: Model
        """
        datasource = self._instantiate(self.params['datasource'])
        training_data = datasource.read_training()
        self._sanity_check(training_data, 'training_data')

        preparator = self._instantiate(self.params['preparator'])
        prepared_data = preparator.prepare(training_data)
        self._sanity_check(prepared_data, 'prepared_data')

        for algo_key, algo_spec in self.params['algorithms'].iteritems():
            algorithm = self._instantiate(algo_spec)
            model = algorithm.train(prepared_data)
            self._sanity_check(model, algo_key + ' model')

            algorithm.persistor.save(model)

    def predict(self, query):
        """Predict a query.

        :param query: Query.
        :return: Prediction.
        """
        predictions = {}

        for algo_key, algo_spec in self.params['algorithms'].iteritems():
            algorithm = self._instantiate(algo_spec)
            model = algorithm.persistor.load()  # TODO: Load once on Workflow
            prediction = algorithm.predict(model, query)
            predictions[algo_key] = prediction

        serving = self._instantiate(self.params['serving'])
        prediction = serving.serve(query, predictions)

        return prediction

    def evaluate(self, query):
        """Evaluate the algorithm.

        :return: List of evaluation info, and tuple of
                 query, predicted result, and actual result.
        """
        pass

    def _instantiate(self, spec):
        """Instantiate class with params.
        """
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
            'algorithm': params['algorithm'],
            'serving': {
                'class': FirstServing,
            },
        })

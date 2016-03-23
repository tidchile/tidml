from abc import ABCMeta, abstractmethod
from tidml.dase.preparator import IdentityPreparator
from tidml.dase.serving import FirstServing
from tidml.utils import Parameterized, load_config, init_spec


class BaseEngine(Parameterized):
    """Abstract base class of engine classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params):

        if params.get('config'):
            filepath = params.get('config')
            params = load_config(filepath)

        super(BaseEngine, self).__init__(params)

    @abstractmethod
    def train(self):
        """Train an algorithm.
        """

    @abstractmethod
    def predict(self, models, query):
        """Predict a query.

        :param query: Query.
        :param models: Models.
        :return: Prediction.
        """

    @abstractmethod
    def evaluate(self, query):
        """Evaluate the algorithm.

        :return: List of evaluation info, and tuple of
                 query, predicted result, and actual result.
        """


class Engine(BaseEngine):
    """Engine default implementation."""

    @property
    def datasource(self):
        return init_spec(self.params['datasource'])

    @property
    def preparator(self):
        return init_spec(self.params.get('preparator', IdentityPreparator))

    @property
    def algorithms(self):
        if self.params.get('algorithm'):
            algorithms = {'': self.params['algorithm']}
        else:
            algorithms = self.params['algorithms']

        for algo_key, algo_spec in algorithms.iteritems():
            algorithm = init_spec(algo_spec)
            yield algo_key, algorithm

    @property
    def serving(self):
        return init_spec(self.params.get('serving', FirstServing))

    def train(self):
        """Train an algorithm.
        """
        training_data = self.datasource.read_training()
        self._sanity_check(training_data, 'training_data')

        prepared_data = self.preparator.prepare(training_data)
        self._sanity_check(prepared_data, 'prepared_data')

        for algo_key, algorithm in self.algorithms:
            model = algorithm.train(prepared_data)
            self._sanity_check(model, algo_key + ' model')

            algorithm.persistor.save(model)

    def load_models(self):
        """Load persisted models.

        :return: Models
        """
        models = {}
        for algo_key, algorithm in self.algorithms:
            model = algorithm.persistor.load()
            models[algo_key] = model
        return models

    def predict(self, models, query):
        """Predict a query.

        :param models: Models.
        :param query: Query.
        :return: Prediction.
        """
        predictions = {}
        for algo_key, algorithm in self.algorithms:
            model = models[algo_key]
            prediction = algorithm.predict(model, query)
            predictions[algo_key] = prediction

        prediction = self.serving.serve(query, predictions)

        return prediction

    def evaluate(self, query):
        """Evaluate the algorithm.

        :return: List of evaluation info, and tuple of
                 query, predicted result, and actual result.
        """

    @staticmethod
    def _sanity_check(data, label):
        # TODO: logging
        if hasattr(data, 'sanity_check'):
            data.sanity_check(label)

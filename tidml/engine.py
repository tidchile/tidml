from abc import ABCMeta, abstractmethod
from tidml.preparator import IdentityPreparator
from tidml.serving import FirstServing
from tidml.utils import Parameterized, load_config, init_spec


class BaseEngine(Parameterized):
    """Abstract base class of engine classes."""

    __metaclass__ = ABCMeta

    def __init__(self, params):

        if params.get('config'):
            filepath = params.get('config')
            params = load_config(filepath)

        if params.get('algorithm'):
            params['algorithms'] = {'': params['algorithm']}

        super(BaseEngine, self).__init__(params)

    @abstractmethod
    def train(self):
        """Train an algorithm.
        """

    @abstractmethod
    def predict(self, query):
        """Predict a query.

        :param query: Query.
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

    def train(self):
        """Train an algorithm.
        """
        datasource = init_spec(self.params['datasource'])
        training_data = datasource.read_training()
        self._sanity_check(training_data, 'training_data')

        preparator = init_spec(self.params.get('preparator', IdentityPreparator))
        prepared_data = preparator.prepare(training_data)
        self._sanity_check(prepared_data, 'prepared_data')

        for algo_key, algo_spec in self.params['algorithms'].iteritems():
            algorithm = init_spec(algo_spec)
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
            algorithm = init_spec(algo_spec)
            model = algorithm.persistor.load()  # TODO: Load once on Workflow
            prediction = algorithm.predict(model, query)
            predictions[algo_key] = prediction

        serving = init_spec(self.params.get('serving', FirstServing))
        prediction = serving.serve(query, predictions)

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

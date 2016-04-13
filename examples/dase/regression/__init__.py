from collections import namedtuple
import numpy as np
from sklearn import datasets, linear_model
from tidml.dase.data_source import DataSource
from tidml.dase.preparator import Preparator
from tidml.dase.algorithm import Algorithm
from tidml.dase.engine import Engine
from tidml.utils import require_argument

PreparedData = namedtuple('PreparedData', 'x, y')
Query = namedtuple('Query', 'x')


class RegressionDataSource(DataSource):
    def read_training(self):
        return datasets.load_diabetes()


class RegressionPreparator(Preparator):
    def prepare(self, training_data):
        require_argument('training_data', training_data)
        take = self.params['take']
        x = training_data.data[:, np.newaxis, 2]
        x_train = x[:take]
        y_train = training_data.target[:take]
        return PreparedData(x=x_train, y=y_train)


class RegressionAlgorithm(Algorithm):
    def train(self, data):
        require_argument('data', data, PreparedData)
        model = linear_model.LinearRegression()
        model.fit(data.x, data.y)
        print model
        return model

    def predict(self, model, query):
        require_argument('model', model, linear_model.LinearRegression)
        require_argument('query', query, Query)
        result = model.predict(query.x)
        return result[0]


class RegressionEngineFactory(object):
    @staticmethod
    def create():
        return Engine({'config': 'examples/dase/regression/config.yaml'})

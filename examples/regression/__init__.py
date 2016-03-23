from collections import namedtuple
import numpy as np
from sklearn import datasets, linear_model
from tidml.data_source import DataSource
from tidml.preparator import Preparator
from tidml.algorithm import Algorithm
from tidml.engine import Engine
from tidml.utils import guard

PreparedData = namedtuple('PreparedData', 'x, y')
Query = namedtuple('Query', 'x')


class RegressionDataSource(DataSource):
    def read_training(self):
        return datasets.load_diabetes()


class RegressionPreparator(Preparator):
    def prepare(self, training_data):
        guard('training_data', training_data)
        take = self.params['take']
        x = training_data.data[:, np.newaxis, 2]
        x_train = x[:take]
        y_train = training_data.target[:take]
        return PreparedData(x=x_train, y=y_train)


class RegressionAlgorithm(Algorithm):
    def train(self, data):
        guard('data', data, PreparedData)
        model = linear_model.LinearRegression()
        model.fit(data.x, data.y)
        print model
        return model

    def predict(self, model, query):
        guard('model', model, linear_model.LinearRegression)
        guard('query', query, Query)
        result = model.predict(query.x)
        return result[0]


class RegressionEngineFactory(object):
    @staticmethod
    def create():
        return Engine({'config': 'examples/regression/config.yaml'})

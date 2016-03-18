from collections import namedtuple
import numpy as np
from sklearn import datasets, linear_model
from tidml.data_source import DataSource
from tidml.preparator import Preparator
from tidml.algorithm import Algorithm
from tidml.engine import Engine

RegressionPreparedData = namedtuple('PreparedData', 'x, y')
RegressionQuery = namedtuple('Query', 'x')


class RegressionDataSource(DataSource):
    def read_training(self):
        return datasets.load_diabetes()


class RegressionPreparator(Preparator):
    def prepare(self, td):
        take = self.params['take']
        x = td.data[:, np.newaxis, 2]
        x_train = x[:take]
        y_train = td.target[:take]
        return RegressionPreparedData(x=x_train, y=y_train)


class RegressionAlgorithm(Algorithm):
    def train(self, data):
        model = linear_model.LinearRegression()
        model.fit(data.x, data.y)
        return model

    def predict(self, model, query):
        result = model.predict(query.x)
        return result[0]


class RegressionEngineFactory(object):
    @staticmethod
    def create():
        return Engine({'config': 'examples/regression/config.yaml'})

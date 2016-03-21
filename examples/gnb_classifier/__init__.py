from collections import namedtuple
from sklearn import datasets, naive_bayes
from tidml.data_source import DataSource
from tidml.algorithm import Algorithm
from tidml.engine import Engine
from tidml.serving import Serving

ClassifierQuery = namedtuple('Query', [
    'sepal_length',
    'sepal_width',
    'petal_length',
    'petal_width',
])
ClassifierPrediction = namedtuple('Prediction', 'species')


class ClassifierDataSource(DataSource):
    def read_training(self):
        return datasets.load_iris()


class ClassifierAlgorithm(Algorithm):
    def train(self, pd):
        model = naive_bayes.GaussianNB()
        model.fit(pd.data, pd.target)
        print model
        return model

    def predict(self, model, query):
        result = model.predict([[
            query.sepal_length,
            query.sepal_width,
            query.petal_length,
            query.petal_width,
        ]])
        return result[0]


class ClassifierServing(Serving):
    def serve(self, query, results):
        species = 'Iris ' + ['setosa', 'virginica', 'versicolor'][results['']]
        return ClassifierPrediction(species=species)


class ClassifierEngineFactory(object):
    @staticmethod
    def create():
        return Engine({'config': 'examples/gnb_classifier/config.yaml'})

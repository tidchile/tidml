from tidml.algorithm import Algorithm
from tidml.data_source import DataSource
from tidml.serving import Serving
from tidml.preparator import Preparator
from tidml.engine import Engine

import numpy as np
from sklearn import linear_model

class HousePricesDataSource(DataSource):
    def read_training(self):
        with open('datos.txt', 'r') as file:
            return file.readlines()

class HousePricesPreparator(Preparator):
    def prepare(self, data):
        return [ map(float, line.split()) for line in data]

class HousePricesPredictor(Algorithm):
    def train(self, data):
        features = []
        known_answer = []

        for d in data:
            features.append(d[:-1])
            known_answer.append(d[-1])

        linear_regression = linear_model.LinearRegression()
        linear_regression.fit(features, known_answer)

        return linear_regression

    def predict(self, model, query):
        return model.predict(np.array(query))[0]

class HousePricesPredictorRandom(Algorithm):
    def train(self, data):
        return sum

    def predict(self, model, query):
        return sum(query)

class HousePricesServing(Serving):
    def serve(self, query, results):
        print results

if __name__ == "__main__":
    engine = Engine({'config': 'config.yaml'})

    engine.train()
    models = engine.load_models()

    engine.predict(models, [0.07, 0.99, 0.0, 0.51, 0.69, 0.77, 0.77, 0.75, 0.44])


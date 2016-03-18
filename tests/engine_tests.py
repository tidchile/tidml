from tidml import *
from unittest import SkipTest

# raise SkipTest

test_data_file = '~/.tidml/tests/data.csv'


def make_test_data():
    from sklearn.datasets import make_classification
    import pandas as pd

    data = make_classification(n_samples=3, n_features=4)
    data = data[0]
    df = pd.DataFrame(data, columns=list("ABCD"))

    ModelPersistor.prepare_path(test_data_file)
    df.to_csv(test_data_file, sep='\t', index=False)


class TestDataSource(DataSource):
    def read_training(self):
        import pandas as pd
        df = pd.read_csv(self._params['csv'], sep='\t')
        return df


class TestPreparator(Preparator):
    def prepare(self, data):
        return data


class TestSimpleAlgorithm(Algorithm):
    def train(self, data):
        return data

    def predict(self, model, query):
        pass


class TestAlgorithm(Algorithm):
    def train(self, data):
        return data

    def predict(self, model, query):
        pass

    @property
    def persistor(self):
        return PandasCsvModelPersistor(self._params)


class PandasCsvModelPersistor(ModelPersistor):
    def save(self, model):
        model.to_csv(self._params['model.csv'], index=False)
        # See more http://pandas.pydata.org/pandas-docs/stable/io.html


engine = Engine


def test_setup():
    make_test_data()
    global engine
    engine = Engine({
        'datasource': {
            'class': "tests.engine_tests.TestDataSource",
            'params': {
                'csv': test_data_file,
            }
        },
        'preparator': {
            'class': TestPreparator,
        },
        'algorithm': {
            'class': TestAlgorithm,
            'params': {
                'model.csv': '~/.tidml/tests/model2.csv',  # custom
            },
        },
    })


def test_train():
    engine.train()


# @SkipTest
def test_evaluate():
    engine.evaluate()


def test_simple_engine():
    e = SimpleEngine({
        'datasource': {
            'class': TestDataSource,
            'params': {
                'csv': test_data_file,
            }
        },
        'algorithm': {
            'class': TestSimpleAlgorithm,
            'params': {
                'model.pickle': '~/.tidml/tests/model.pkl',  # default built-in
            },
        },
    })
    e.train()

import nose.tools as nt
from unittest import SkipTest
from tidml.model_persistor import ModelPersistor
from tidml.data_source import DataSource
from tidml.preparator import Preparator
from tidml.algorithm import Algorithm
from tidml.engine import BaseEngine, Engine
from tidml.utils import prepare_path

# raise SkipTest

test_data_file = '~/.tidml/tests/data.csv'


def make_test_data():
    from sklearn.datasets import make_classification
    import pandas as pd

    data = make_classification(n_samples=3, n_features=4)
    data = data[0]
    df = pd.DataFrame(data, columns=list("ABCD"))

    prepare_path(test_data_file)
    df.to_csv(test_data_file, sep='\t', index=False)


class DataWithSanityCheck(object):
    def __init__(self, params, payload):
        self._params = params
        self._payload = payload

    @property
    def payload(self):
        return self._payload

    def sanity_check(self, label):
        """Force "insanity" by params, just for testing."""
        insane = self._params.get('insane', False)
        if insane:
            raise RuntimeError(label + ' insane!')


class TestDataSource(DataSource):
    def read_training(self):
        import pandas as pd
        df = pd.read_csv(self.params['csv'], sep='\t')
        return DataWithSanityCheck(self.params, df)


class TestPreparator(Preparator):
    def prepare(self, data):
        return DataWithSanityCheck(self.params, data.payload)


class TestSimpleAlgorithm(Algorithm):
    def train(self, data):
        return DataWithSanityCheck(self.params, data.payload)

    def predict(self, model, query):
        return query * 2


class TestAlgorithm(Algorithm):
    def train(self, data):
        return DataWithSanityCheck(self.params, data.payload)

    def predict(self, model, query):
        pass

    @property
    def persistor(self):
        return PandasCsvModelPersistor(self.params)


class PandasCsvModelPersistor(ModelPersistor):
    # See more http://pandas.pydata.org/pandas-docs/stable/io.html

    def __init__(self, params):
        super(PandasCsvModelPersistor, self).__init__(params)
        self._path = params['model.csv']

    def load(self):
        import pandas
        data = pandas.read_csv(self._path)
        return DataWithSanityCheck(self.params, data)

    def save(self, model):
        model.payload.to_csv(self._path, index=False)


engine = Engine


def test_setup():
    make_test_data()
    global engine
    engine = Engine({
        'datasource': {
            'class': TestDataSource,
            'params': {
                'csv': test_data_file,
            },
        },
        'preparator': TestPreparator,
        'algorithm': {
            'class': TestAlgorithm,
            'params': {
                'model.csv': '~/.tidml/tests/model2.csv',  # custom
            },
        },
    })


def test_train():
    engine.train()


def test_simple_engine():
    e = Engine({
        'datasource': {
            'class': TestDataSource,
            'params': {
                'csv': test_data_file,
            },
        },
        'algorithm': {
            'class': TestSimpleAlgorithm,
            'params': {
                'model.pickle': '~/.tidml/tests/model.pkl',  # default built-in
            },
        },
    })
    e.train()
    prediction = e.predict(3)
    nt.assert_equals(prediction, 6)


def test_insane_datasource():
    e = Engine({
        'datasource': {
            'class': TestDataSource,
            'params': {
                'csv': test_data_file,
                'insane': True,
            },
        },
    })
    nt.assert_raises_regexp(RuntimeError, 'training_data insane!', e.train)


def test_insane_preparator():
    e = Engine({
        'datasource': {
            'class': TestDataSource,
            'params': {
                'csv': test_data_file,
            },
        },
        'preparator': {
            'class': TestPreparator,
            'params': {
                'insane': True,
            },
        },
    })
    nt.assert_raises_regexp(RuntimeError, 'prepared_data insane!', e.train)


def test_insane_algorithm():
    e = Engine({
        'datasource': {
            'class': TestDataSource,
            'params': {
                'csv': test_data_file,
            },
        },
        'preparator': TestPreparator,
        'algorithm': {
            'class': TestAlgorithm,
            'params': {
                'model.csv': '~/.tidml/tests/model2.csv',  # custom
                'insane': True,
            },
        },
    })
    nt.assert_raises_regexp(RuntimeError, 'model insane!', e.train)


def test_train():
    engine.train()


class TestEngine(BaseEngine):
    def train(self):
        pass

    def predict(self, query):
        super(TestEngine, self).predict(query)

    def evaluate(self):
        pass


test_config = {
    'datasource': {
        'class': 'TestDataSource',
        'params': {
            'take': 100
        }
    }
}


def test_base_engine_loads_yaml():
    import tempfile, yaml
    with tempfile.NamedTemporaryFile(suffix='.yaml') as temp:
        temp.write(yaml.dump(test_config))
        temp.flush()
        e = TestEngine({'config': temp.name})
        nt.assert_equals(e.params, test_config)


def test_base_engine_loads_json():
    import tempfile, json
    with tempfile.NamedTemporaryFile(suffix='.json') as temp:
        temp.write(json.dumps(test_config))
        temp.flush()
        e = TestEngine({'config': temp.name})
        nt.assert_equals(e.params, test_config)


def test_base_engine_loads_not_supported_format():
    import tempfile, json
    with tempfile.NamedTemporaryFile(suffix='.xml') as temp:
        nt.assert_raises_regexp(
            NotImplementedError,
            'Not implemented config format \.xml',
            TestEngine, {'config': temp.name}
        )

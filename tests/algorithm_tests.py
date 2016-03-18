import nose.tools as nt
from tidml.algorithm import *

from unittest import SkipTest


def test_cannot_instantiate():
    nt.assert_raises(TypeError, Algorithm)


class TestAlgorithm(Algorithm):
    def train(self, data):
        pass

    def predict(self, model, query):
        pass


class TestAlgorithmWithCustomPersistor(Algorithm):
    def train(self, data):
        pass

    def predict(self, model, query):
        pass

    @property
    def persistor(self):
        class CustomModelPersistor(ModelPersistor):
            def save(self, model):
                pass

        return CustomModelPersistor()


def test_init_empty_params():
    ds = TestAlgorithm()
    nt.assert_equals(ds.params, {})


def test_init_params():
    ds = TestAlgorithm({'p1': 'A'})
    nt.assert_equals(ds.params, {'p1': 'A'})


def test_default_pickle_model_persistor():
    ds = TestAlgorithm({'model.pickle': ''})
    nt.assert_is_instance(ds.persistor, PickleModelPersistor)


def test_with_custom_model_persistor():
    ds = TestAlgorithmWithCustomPersistor()
    nt.assert_is_instance(ds.persistor, ModelPersistor)


def test_builtin_pickle_model_persistor():
    p = PickleModelPersistor({'model.pickle': '~/.tidml/builtin.pkl'})
    p.save([1, 2, 3])


def test_pandas_pickle_model_persistor():
    p = PickleModelPersistor({'model.pickle': '~/.tidml/pandas.pkl'})
    import pandas as pd
    df = pd.DataFrame([1, 2, 3])
    p.save(df)

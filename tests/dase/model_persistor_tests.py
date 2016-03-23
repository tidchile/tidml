import nose.tools as nt
from tidml.dase.model_persistor import ModelPersistor, PickleModelPersistor

from unittest import SkipTest


def test_cannot_instantiate():
    nt.assert_raises(TypeError, ModelPersistor)


class TestModelPersistor(ModelPersistor):
    def load(self):
        pass

    def save(self, model):
        pass


def test_init_empty_params():
    ds = TestModelPersistor()
    nt.assert_equals(ds.params, {})


def test_init_params():
    ds = TestModelPersistor({'p1': 'A'})
    nt.assert_equals(ds.params, {'p1': 'A'})


def test_builtin_pickle_model_persistor():
    p = PickleModelPersistor({'model.pickle': '~/.tidml/builtin.pkl'})
    p.save([1, 2, 3])


def test_pandas_pickle_model_persistor():
    p = PickleModelPersistor({'model.pickle': '~/.tidml/pandas.pkl'})
    import pandas as pd
    df = pd.DataFrame([1, 2, 3])
    p.save(df)

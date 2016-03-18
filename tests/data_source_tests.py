import nose.tools as nt
from tidml.data_source import DataSource

from unittest import SkipTest


def test_cannot_instantiate():
    nt.assert_raises(TypeError, DataSource)


class TestDataSource(DataSource):
    def read_training(self):
        pass


def test_init_empty_params():
    ds = TestDataSource()
    nt.assert_equals(ds.params, {})


def test_init_params():
    ds = TestDataSource({'p1': 'A'})
    nt.assert_equals(ds.params, {'p1': 'A'})

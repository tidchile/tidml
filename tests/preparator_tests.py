import nose.tools as nt
from tidml.preparator import Preparator, IdentityPreparator

from unittest import SkipTest


def test_cannot_instantiate():
    nt.assert_raises(TypeError, Preparator)


class TestPreparator(Preparator):
    def prepare(self, data):
        sep = self.params['sep']
        return sep + data.upper() + sep


def test_init_empty_params():
    ds = TestPreparator()
    nt.assert_equals(ds.params, {})


def test_init_params():
    ds = TestPreparator({'p1': 'A'})
    nt.assert_equals(ds.params, {'p1': 'A'})


def test_prepare():
    sut = TestPreparator({'sep': '*'})
    result = sut.prepare('the data')
    nt.assert_equals(result, '*THE DATA*')


def test_identity_preparator():
    sut = IdentityPreparator()
    result = sut.prepare('the data')
    nt.assert_equals(result, 'the data')

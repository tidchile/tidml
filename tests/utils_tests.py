import nose.tools as nt
from tidml.utils import prepare_path, init_spec, Parameterized


def test_prepare_path():
    import os
    import shutil
    base_path = '~/.tidml/prepared_path/'
    file_name = 'the_file'
    shutil.rmtree(os.path.expanduser(base_path), ignore_errors=True)
    pp = prepare_path(base_path + file_name)
    nt.assert_regexp_matches(pp, '/Users/(.)+/\.tidml/prepared_path/the_file')


class TestParameterizedClass(Parameterized):
    pass


class TestNotParameterizedClass(object):
    pass


def test_init_string_spec():
    instance = init_spec('tests.utils_tests.TestParameterizedClass')
    nt.assert_equals(instance.params, {})


def test_init_class_spec():
    instance = init_spec(TestParameterizedClass)
    nt.assert_equals(instance.params, {})


def test_init_dict_string_spec():
    instance = init_spec({
        'class': 'tests.utils_tests.TestParameterizedClass'
    })
    nt.assert_equals(instance.params, {})


def test_init_dict_class_spec():
    instance = init_spec({
        'class': TestParameterizedClass
    })
    nt.assert_equals(instance.params, {})


def test_init_dict_class_with_params_spec():
    instance = init_spec({
        'class': TestParameterizedClass,
        'params': {'p1': 123}
    })
    nt.assert_equals(instance.params, {'p1': 123})


def test_init_spec_subclass_error():
    nt.assert_raises_regexp(
        RuntimeError,
        "'TestNotParameterizedClass' is not subclass of 'Parameterized'",
        init_spec, TestNotParameterizedClass)

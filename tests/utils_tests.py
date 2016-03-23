import nose.tools as nt
from tidml.utils import prepare_path, init_spec, Parameterized, extend, guard


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


def test_extend():
    from collections import namedtuple

    named_tuple = namedtuple('NamedTuple', 'a, b')

    @extend(named_tuple)
    def c(self):
        return self.a + self.b

    class AnotherClass(object):
        def __init__(self):
            self.a = 1
            self.b = 6

    t = named_tuple(a=2, b=3)
    x = AnotherClass()

    @extend(t, x, name='d')
    def the_method_to_extend(self):
        return self.a * self.b

    nt.assert_equals(t.c(), 5)
    nt.assert_equals(t.d(), 6)
    nt.assert_equals(x.d(), 6)


def test_guard_pass_none():
    guard('arg', 123)


def test_guard_pass_type():
    guard('arg', 123, int)


def test_guard_fail_none():
    nt.assert_raises_regexp(
        TypeError,
        "Argument 'arg' should have a value",
        guard, 'arg', None
    )


def test_guard_fail_type():
    nt.assert_raises_regexp(
        TypeError,
        "Argument 'arg' should be <type 'str'>",
        guard, 'arg', 123, str
    )

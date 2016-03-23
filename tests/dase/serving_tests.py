import nose.tools as nt
from tidml.dase.serving import Serving, FirstServing, AverageServing


def test_serving():
    class TestIdentityServing(Serving):
        def serve(self, query, results):
            return query, results

    serving = TestIdentityServing()
    result = serving.serve('query', 'results')
    nt.assert_equals(result, ('query', 'results'))


def test_first_serving():
    serving = FirstServing()
    result = serving.serve(None, {'a': 'A', 'b': 'B'})
    nt.assert_equals(result, 'A')


def test_average_serving():
    serving = AverageServing()
    result = serving.serve(None, {'a': 10, 'b': 11})
    nt.assert_equals(result, 10.5)

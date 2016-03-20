from examples.regression import RegressionEngineFactory
from examples.regression import RegressionQuery as Query


def main():
    e = RegressionEngineFactory.create()
    e.train()
    models = e.load_models()
    print e.predict(models, Query(x=0.07))
    print e.predict(models, Query(x=-0.03))
    print e.predict(models, Query(x=1))


if __name__ == '__main__':
    main()

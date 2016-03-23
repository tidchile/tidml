from examples.regression import RegressionEngineFactory
from examples.regression import Query


def main():
    engine = RegressionEngineFactory.create()
    engine.train()
    models = engine.load_models()
    print engine.predict(models, Query(x=0.07))
    print engine.predict(models, Query(x=-0.03))
    print engine.predict(models, Query(x=1))


if __name__ == '__main__':
    main()

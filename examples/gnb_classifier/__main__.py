from examples.gnb_classifier import ClassifierEngineFactory
from examples.gnb_classifier import Query


def main():
    engine = ClassifierEngineFactory.create()
    engine.train()
    models = engine.load_models()
    predict(engine, models, Query(
        sepal_length=6,
        sepal_width=3.5,
        petal_length=5,
        petal_width=2,
    ))
    predict(engine, models, Query(
        sepal_length=4,
        sepal_width=3,
        petal_length=1,
        petal_width=0.1,
    ))
    predict(engine, models, Query(
        sepal_length=7,
        sepal_width=3,
        petal_length=5,
        petal_width=1.1,
    ))


def predict(engine, models, query):
    print '\n', query, '\n', engine.predict(models, query)


if __name__ == '__main__':
    main()

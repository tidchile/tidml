from examples.hello_world import MyEngineFactory, MyQuery


def main():
    engine = MyEngineFactory.create()
    engine.train()
    models = engine.load_models()
    prediction = engine.predict(models, MyQuery(day='mon'))
    print prediction


if __name__ == '__main__':
    main()

from examples.hello_world import MyEngineFactory, MyQuery


def main():
    e = MyEngineFactory.create()
    e.train()
    models = e.load_models()
    prediction = e.predict(models, MyQuery(day='mon'))
    print prediction


if __name__ == '__main__':
    main()

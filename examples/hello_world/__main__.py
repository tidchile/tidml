from examples.hello_world import MyEngineFactory, MyQuery


def main():
    e = MyEngineFactory.create()
    e.train()
    prediction = e.predict(MyQuery(day='mon'))
    print prediction


if __name__ == '__main__':
    main()

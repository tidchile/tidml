from tidml.dase.engine import Engine


def main():
    engine = Engine({'config': 'examples/dase/house_prices/config.yaml'})

    engine.train()
    models = engine.load_models()

    engine.predict(
        models,
        [0.07, 0.99, 0.0, 0.51, 0.69, 0.77, 0.77, 0.75, 0.44]
    )


if __name__ == '__main__':
    main()

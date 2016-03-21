# Linear Regression Engine

## Run

```
python -m examples.regression
```

## Configuration

This example uses a YAML file (`config.yaml`) to configure the engine,
including which classes implement each component and parameter values.

## DataSource

Training data is the *diabetes* dataset built in scikit-learn.

## Preparator

In this example, preparator takes a parameter `take`
to specify how many data points use.

## Algorithm

This is a wrapper around scikit-learn to train a linear regression model.

By default, the model is persisted to a file using pickle format
(see `PickleModelPersistor`). The file path is configured
with parameter `model.pickle`.


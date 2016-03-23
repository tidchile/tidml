Gaussian Naive Bayes Classifier Engine
======================================

Run
---

::

    python -m examples.dase.gnb_classifier

Configuration
-------------

This example uses a YAML file (``config.yaml``) to configure the engine,
including which classes implement each component and parameter values.

DataSource
----------

Training data is the *iris* dataset built in scikit-learn.

Preparator
----------

This example does not implement a preparator, so the default one is used
(``IdentityPreparator``) which just passes the training data through.

Algorithm
---------

This is a wrapper around scikit-learn to train a gaussian naive bayes
model.

By default, the model is persisted to a file using pickle format (see
``PickleModelPersistor``). The file path is configured with parameter
``model.pickle``.

Serving
-------

In this example, serving class converts the species code to species
name, making it more presentable.

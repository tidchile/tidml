# TODO: Multinomial Naive Bayes classifier example
# TODO: Evaluation / Hyperparameter tuning
# TODO: Incremental training (partial_fit)
# TODO: CLI
# TODO: Flask/Django/other microservice
# TODO: Docker/other deployment
# TODO: H2O.ai integration

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'TID ML',
    'author': 'Ricardo Stuven',
    'url': '',
    'download_url': 'Where to download it.',
    'author_email': 'ricardo.stuven@telefonica.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['tidml'],
    'scripts': [],
    'name': 'tidml'
}

setup(**config)

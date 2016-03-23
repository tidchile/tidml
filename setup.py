# -*- coding: utf-8 -*-
import sys
import pip
from os import path
from codecs import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def read(filepath):
    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, filepath), encoding='utf-8') as f:
        return f.read()


version = read('VERSION').replace('\n', '')

if sys.argv[1] == 'install':
    # install package dependencies only
    pip.main(['install', '-r', 'requirements.txt'])

setup(
    name='tidml',
    description='Telefónica I+D Machine Learning Workflow Framework',
    long_description=read('README.rst'),
    author='Ricardo Stuven',
    author_email='ricardo.stuven@telefonica.com',
    url='https://github.com/tidchile/tidml',
    download_url='https://github.com/tidchile/tidml/tarball/' + version,
    version=version,
    packages=['tidml'],
    scripts=[],
    test_suite='nose.collector',
    # TODO: classifiers= []
    # TODO: keywords=''
    # TODO: license=''
    # DON'T USE install_requires or tests_require.
    # They do not resolve dependencies order right.
    # eg. numpy as precondition of scikit_learn
)

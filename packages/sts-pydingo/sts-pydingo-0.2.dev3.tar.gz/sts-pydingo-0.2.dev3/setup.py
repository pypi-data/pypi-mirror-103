import os

from setuptools import setup

setup(name = 'sts-pydingo', description = 'Client library', author = 'See-Through Scientific',
    packages = ['pydingo'], install_requires = ['pillow', 'tornado', 'zeroconf'],
    use_scm_version = {'local_scheme': 'no-local-version', 'write_to': os.path.join('pydingo', 'version.py')})

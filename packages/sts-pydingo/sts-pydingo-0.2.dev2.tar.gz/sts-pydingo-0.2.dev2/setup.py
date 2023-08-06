from setuptools import setup

#from setuptools_scm import get_version
# 'write_to': 'version.py'

setup(name = 'sts-pydingo', description = 'Client library', author = 'See-Through Scientific',
    packages = ['pydingo'], install_requires = ['pillow', 'tornado', 'zeroconf'],
    use_scm_version = {'local_scheme': 'no-local-version', 'write_to': 'pydingo/version.py'})

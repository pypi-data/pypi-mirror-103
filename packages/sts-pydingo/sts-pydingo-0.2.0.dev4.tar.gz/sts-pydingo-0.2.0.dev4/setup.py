import os

from setuptools import setup

use_scm_version = {
    'version_scheme': 'release-branch-semver',
    'local_scheme': 'no-local-version',
    'write_to': os.path.join('pydingo', 'version.py')
}

setup(name = 'sts-pydingo', description = 'Client library', author = 'See-Through Scientific',
    packages = ['pydingo'], install_requires = ['pillow', 'tornado', 'zeroconf'],
    use_scm_version = use_scm_version)

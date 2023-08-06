# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['qaa', 'qaa.commands', 'qaa.decomposition', 'qaa.libs']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'holoviews[recommended]>=1.14.3,<2.0.0',
 'mdtraj>=1.9,<2.0',
 'nptyping>=1.4,<2.0',
 'scikit-learn>=0.24,<0.25']

extras_require = \
{'jupyter': ['jupyter>=1.0.0,<2.0.0',
             'jupyterlab>=3.0.13,<4.0.0',
             'jupyterlab-code-formatter>=1.4.10,<2.0.0',
             'jupyterlab-mathjax3>=4.2.2,<5.0.0',
             'nglview>=3.0.0,<4.0.0',
             'plotly>=4.14.3,<5.0.0']}

entry_points = \
{'console_scripts': ['qaa = qaa.__main__:main']}

setup_kwargs = {
    'name': 'qaa',
    'version': '1.0.0rc1',
    'description': 'Quasi-Anharmonic Analysis',
    'long_description': 'Quasi-Anharmonic Analysis\n=========================\n\n|PyPI| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/qaa.svg\n   :target: https://pypi.org/project/qaa/\n   :alt: PyPI\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/qaa\n   :target: https://pypi.org/project/qaa\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/qaa\n   :target: https://opensource.org/licenses/BSD-3-Clause\n   :alt: License\n.. |Read the Docs| image:: https://readthedocs.org/projects/pyqaa/badge/?version=latest\n   :target: https://pyqaa.readthedocs.io/en/latest/?badge=latest\n   :alt: ReDocumentation Status\n.. |Tests| image:: https://github.com/tclick/qaa/workflows/Tests/badge.svg\n   :target: https://github.com/tclick/qaa/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/tclick/qaa/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/tclick/qaa\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. image:: https://pyup.io/repos/github/tclick/qaa/shield.svg\n     :target: https://pyup.io/repos/github/tclick/qaa/\n     :alt: Updates\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\nFeatures\n--------\n\n`qaa` analyzes molecular dynamics (MD) trajectories by using joint\ndiagonalization (JADE) to separate the information. The JADE [1]_ and QAA [2]_\ncode are based on the original code written in Matlab.\n\n.. [1] Cardoso, J. F.; Souloumiac, A. "Blind Beamforming for Non-Gaussian\n       Signals." IEE Proc F Radar Signal Process 1993, 140 (6), 362.\n.. [2] Ramanathan, A.; Savol, A. J.; Langmead, C. J.; Agarwal, P. K.;\n       Chennubhotla, C. S. "Discovering Conformational Sub-States Relevant to Protein\n       Function." Plos One 2011, 6 (1), e15827.\n\nRequirements\n------------\n\n* Python 3.8+\n* click 7.0+\n* numpy 1.20+\n* scipy 1.6+\n* matplotlib 3.3+\n* scikit-learn 0.24+\n* mdtraj 1.9+\n* nptyping 1.4+\n* holoviews 1.14+\n\nInstallation\n------------\n\nYou can install *Quasi-Anharmonic Analysis* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install qaa\n\nIf you want to visualize the tutorial notebooks, you can install the extra\ndependencies via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install qaa[jupyter]\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `BSD 3 Clause license`_,\n*Quasi-Anharmonic Analysis* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from `@cjolowicz`_\'s `Hypermodern Python Cookiecutter`_ template.\n\n.. _@cjolowicz: https://github.com/cjolowicz\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _BSD 3 Clause license: https://opensource.org/licenses/BSD-3-Clause\n.. _PyPI: https://pypi.org/\n.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n.. _file an issue: https://github.com/tclick/qaa/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://qaa.readthedocs.io/en/latest/usage.html\n',
    'author': 'Timothy H. Click',
    'author_email': 'tclick@okstate.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tclick/qaa',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)

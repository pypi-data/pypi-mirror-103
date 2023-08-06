# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kuibit']

package_data = \
{'': ['*'], 'kuibit': ['data/*']}

install_requires = \
['ConfigArgParse>=1.2.3,<2.0.0',
 'h5py>=2.9.0',
 'numpy>=1.18.5,<2.0.0',
 'scipy>=1.5.2,<2.0.0']

extras_require = \
{'full': ['numba>=0.51.2,<0.52.0',
          'lalsuite>=6.77,<7.0',
          'pycbc>=1.16.10,<2.0.0']}

setup_kwargs = {
    'name': 'kuibit',
    'version': '1.1.1',
    'description': 'Read and analyze Einstein Toolkit simulations.',
    'long_description': '<p align="center">\n<img src="https://github.com/Sbozzolo/kuibit/raw/master/logo.png" height="120">\n</p>\n\n[![DOI](https://joss.theoj.org/papers/10.21105/joss.03099/status.svg)](https://doi.org/10.21105/joss.03099)\n[![codecov](https://codecov.io/gh/Sbozzolo/kuibit/branch/master/graph/badge.svg)](https://codecov.io/gh/Sbozzolo/kuibit)\n![Tests](https://github.com/Sbozzolo/kuibit/workflows/Tests/badge.svg)\n![Documentation](https://github.com/Sbozzolo/kuibit/workflows/Document/badge.svg)\n[![GPLv3\nlicense](https://img.shields.io/badge/License-GPLv3-blue.svg)](http://perso.crans.org/besson/LICENSE.html)\n[![Get help on Telegram](https://img.shields.io/badge/Get%20help%20on-Telegram-blue.svg)](https://t.me/kuibit)\n[![PyPI version](https://badge.fury.io/py/kuibit.svg)](https://badge.fury.io/py/kuibit)\n[![DeepSource](https://deepsource.io/gh/Sbozzolo/kuibit.svg/?label=active+issues)](https://deepsource.io/gh/Sbozzolo/kuibit/?ref=repository-badge)\n\n# kuibit\n\n`kuibit` is a Python library to analyze simulations performed with the Einstein\nToolkit largely inspired by\n[PostCactus](https://github.com/wokast/PyCactus/tree/master/PostCactus).\n`kuibit` can read simulation data and represent it with high-level classes. For\na list of features available, look at the [official\ndocumentation](https://sbozzolo.github.io/kuibit). For examples and tools that\nare ready to be used, read the [Experimental branch and examples\nsection](https://github.com/Sbozzolo/kuibit/#experimental-branch-and-examples).\nThe [testimonials page](https://sbozzolo.github.io/kuibit/testimonials.html)\ncollects short reviews about `kuibit`.\n\n## Installation\n\n``kuibit`` is available in PyPI. To install it with `pip`\n``` bash\npip3 install kuibit\n```\nIf they are not already available, `pip` will install all the necessary dependencies.\n\nThe minimum version of Python required is 3.6.\n\nIf you intend to develop ``kuibit``, follow the instruction below.\n\n### Development\n\nFor development, we use [poetry](https://python-poetry.org/). Poetry simplifies\ndependency management, building, and publishing the package.\n\nTo install `kuibit` with poetry, clone this repo, move into the folder, and run:\n``` sh\npoetry install -E full\n```\nThis will download all the needed dependencies in a sandboxed environment (the\n`-E full` flag is for the optional dependencies). When you want to use\n``kuibit``, just run ``poetry shell`` from within the `kuibit` directory.\nThis will drop you in a shell in\nwhich you have full access to ``kuibit`` in "development" version, and its\ndependencies (including the one needed only for development). Alternatively, you\ncan activate the virtual environment directly. You can find where the environment\nin installed running the command `poetry env info --path` in the `kuibit` directory.\nThis is a standard virtual environment, which can be activated with the `activate`\nscripts in the `bin` folder. Once you do that, you will be able to use `kuibit`\nfor anywhere.\n\n## Help!\n\nUsers and developers of ``kuibit`` meet in the [Telegram\ngroup](https://t.me/kuibit). If you have any problem or suggestion, that\'s a\ngood place where to discuss it. Alternatively, you can also open an issue on\nGitHub.\n\n## Documentation\n\n`kuibit` uses Sphinx to generate the documentation. To produce the documentation\n```sh\ncd docs && make html\n```\nDocumentation is automatically generated after each commit by GitHub Actions.\n\nWe use [nbsphinx](https://nbsphinx.readthedocs.io/) to translate Jupyter\nnotebooks to the examples. The extension is required. Note: Jupyter notebooks\nhave to be un-evaluated. `nbsphinx` requires [pandoc](https://pandoc.org/). If\ndon\'t have `pandoc`, you should comment out `nbsphinx` in `docs/conf.py`, or\ncompiling the documentation will fail.\n\n## Videos\n\nHere is a list of videos describing `kuibit` and how to use it:\n- [Introduction on kuibit - Einstein Toolkit Seminar, 2021](https://www.youtube.com/watch?v=7-F2xh-m31A)\n\n## Tests\n\n`kuibit` comes with a suite of unit tests. To run the tests, (in a poetry shell),\n```sh\npoetry run python -m unittest\n```\nTests are automatically run after each commit by GitHub Actions.\n\nIf you want to look at the coverage of your tests, run (in a poetry shell)\n```sh\ncoverage run -m unittest\ncoverage html\n```\nThis will produce a directory with the html files containing the analysis of\nthe coverage of the tests.\n\n## Experimental branch and examples\n\nThe git repo of `kuibit` has an `experimental` branch, which contains the\nversion of `kuibit` that is currently under development (which will become\n`1.1.0`). The main new features added are new modules to produce visualizations\nand to write non-interactive scripts. The branch also collects a large number of\nreal-world scripts in the folder\n[examples](https://github.com/Sbozzolo/kuibit/tree/experimental/examples). When\nusing `kuibit 1.1.0`, these codes are ready to be used for scientific analyses.\nHowever, given that the scripts rely on the `experimental` features only for\nparsing command-line arguments and to produce visualizations, the codes are also\nan excellent material to learn how to use the current stable version of\n`kuibit`.\n\n## What is a _kuibit_?\n\nA kuibit (also known as _kukuipad_, meaning harvest pole) is the tool\ntraditionally used by the Tohono O\'odham people to reach the fruit of the\nSaguaro cacti during the harvesting season. In the same way, this package is a\ntool that you can use to collect the fruit of your `Cactus` simulations.\n\n## Credits\n\n`kuibit` follows the same design and part of the implementation details of\n`PostCactus`, code developed by Wolfgang Kastaun. This fork completely rewrites\nthe original code, adding emphasis on documentation, testing, and extensibility.\nThe logo contains elements designed by [freepik.com](freepik.com). We thank\n``kuibit`` first users, Stamatis Vretinaris and Pedro Espino, for providing\ncomments to improve the code and the documentation.\n\n## Citation\n\n`kuibit` is built and maintained by the dedication of one graduate student. Please,\nconsider citing `kuibit` if you find the software useful. You can use the following\n`bibtex` key.\n``` bibtex\n@article{kuibit,\n  doi = {10.21105/joss.03099},\n  url = {https://doi.org/10.21105/joss.03099},\n  year = {2021},\n  publisher = {The Open Journal},\n  volume = {6},\n  number = {60},\n  pages = {3099},\n  author = {Gabriele Bozzola},\n  title = {kuibit: Analyzing Einstein Toolkit simulations with Python},\n  journal = {Journal of Open Source Software},\n  archivePrefix = {arXiv},\n  eprint = {2104.06376},\n  primaryClass = {gr-qc}\n}\n```\nYou can find this entry in Python with `from kuibit import __bibtex__`.\n',
    'author': 'Gabriele Bozzola',
    'author_email': 'gabrielebozzola@arizona.edu',
    'maintainer': 'Gabriele Bozzola',
    'maintainer_email': 'gabrielebozzola@arizona.edu',
    'url': 'https://github.com/sbozzolo/kuibit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)

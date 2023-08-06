# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trattoria']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.19.5', 'scipy==1.5.4', 'trattoria-core==0.1.0']

setup_kwargs = {
    'name': 'trattoria',
    'version': '0.1.1',
    'description': 'The fastest streaming algorithms for your TTTR data',
    'long_description': '# Trattoria\n🍕\nTrattoria delivers you the fastest streaming algorithms to analyze your TTTR data. We\ncurrenlty support the following algorithms:\n- Second order autocorrelations: Calculate the autocorrelation between two channels of\n  your TCSPC.\n- Intensity time trace: Calculate the intensity on each (or all) channels versus time.\n- Zero finder: Given two uncorrelated channels (e.g. a laser behind a 50/50 splitter)\n  compute the delay between the input channels.\n\n## Supported file formats\nCurrently Trattoria can only read PTU files from PicoQuant. If you want support for more\nor want to help providing it please put a ticket on the tttr-toolbox project.\n\n## Installing\n```\npip install trattoria\n```\n\n## Examples\nThe entry point to Trattoria is the PTUFile class. This class has three methods that\ngive us access to the algorithms. Each of the algorithms takes as input a parameter\nobject and returns a results object. For example:\n```python\nimport trattoria\n\nimport matplotlib.pyplot as plt\n\nptu_filepath = Path("/path/to/some.ptu")\nptu = trattoria.PTUFile(ptu_filepath)\n\ntimetrace_params = trattoria.TimeTraceParameters(\n    resolution=10.0,\n    channel=None,\n)\ntt_res = ptu.timetrace(timetrace_params)\n\nplt.plot(tt_res.t, tt_res.tt / timetrace_params.resolution)\nplt.xlabel("Time (s)")\nplt.ylabel("Intensity (Hz)")\nplt.show()\n```\n\nThe examples folders contains examples of all the functionality available in Trattoria.\nFor more details check the docstrings in `core.py`.\n\n## Design\nTrattoria is just a very thing wrapper around the trattoria-core library which itselfs provides\na lower level interface to the the tttr-toolbox library. A Rust project that provides\nthe compiled components that allows us to go fast.\n\n## Citing\n',
    'author': 'Guillem Ballesteros',
    'author_email': 'dev+pypi@maxwellrules.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/GCBallesteros/trattoria',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

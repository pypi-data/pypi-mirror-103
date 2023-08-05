# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_hplc']

package_data = \
{'': ['*']}

install_requires = \
['pyserial>=3.5,<4.0']

setup_kwargs = {
    'name': 'py-hplc',
    'version': '0.1.5',
    'description': 'An unoffical Python wrapper for the SSI-Teledyne Next Generation class HPLC pumps.',
    'long_description': '========================================================================\npy-hplc |license| |python| |pypi| |build-status| |docs| |pylint| |style| \n========================================================================\n\nOverview\n==========\nAn unoffical Python wrapper for the SSI-Teledyne Next Generation class HPLC pumps.\n\n- `Download page`_ \n- `API Documentation`_\n- `Official pump documentation`_\n\nMIT license, (C) 2021 Alex Whittington <alex@southsun.tech>\n\nInstallation\n=============\nThe package is available on PyPI.\n\n``pip install py-hplc``\n\n\n\nUsing the package\n==================\n\n.. image:: https://raw.githubusercontent.com/teauxfu/py-hplc/main/docs/demo.gif\n  :alt: gif demonstrating example usage\n\nYou can open a pump instance like this ::\n\n   >>> from py_hplc import NextGenPump\n   >>> pump = NextGenPump("COM3")  # or "/dev/ttyUSB0", etc.\n\nYou can inspect the pump for useful information such as its pressure units, firmware version, max flowrate, etc. ::\n\n   >>> pump.version\n   \'191017 Version 2.0.8\'\n   >>> pump.pressure_units\n   \'psi\'\n   >>> pump.pressure\n   100\n\nThe interface behaves in a typical way. Pumps can be inspected or configured without the use of getters and setters. ::\n\n    >>> pump.flowrate\n    10.0\n    >>> pump.flowrate = 5.5  # mL / min\n    >>> pump.flowrate\n    5.5\n    >>> pump.run()\n    >>> pump.is_running\n    True\n    >>> pump.stop()\n    >>> pump.is_running\n    False\n    >>> pump.leak_detected\n    False\n\n| Some pump commands, such as "CC" (current conditions), return many pieces of data at once.\n| This package makes the data available in concise, descriptive, value-typed dictionaries. \n\n::\n\n   >>> pump.current_conditions()\n   {\'response\': \'OK,0000,10.00/\', \'pressure\': 0, \'flowrate\': 10.0}\n   >>> pump.read_faults()\n   {\'response\': \'OK,0,0,0/\', \'motor stall fault\': False, \'upper pressure fault\': False, \'lower pressure fault\': False}\n\nSee the `API Documentation`_ for more usage examples.\n\n.. _`Download page`: https://pypi.org/project/py-hplc/\n\n.. _`API Documentation`: https://py-hplc.readthedocs.io/en/latest/\n\n.. _`Official pump documentation`: https://www.teledynessi.com/Manuals%20%20Guides/Product%20Guides%20and%20Resources/Serial%20Pump%20Control%20for%20Next%20Generation%20SSI%20Pumps.pdf\n\n.. |license| image:: https://img.shields.io/github/license/teauxfu/py-hplc \n  :target: https://github.com/teauxfu/py-hplc/blob/main/LICENSE.txt\n  :alt: GitHub\n\n.. |python| image:: https://img.shields.io/pypi/pyversions/py-hplc   \n  :alt: PyPI - Python Version\n  \n.. |pypi| image:: https://img.shields.io/pypi/v/py-hplc   \n  :target: https://pypi.org/project/py-hplc/\n  :alt: PyPI\n\n.. |build-status| image:: https://github.com/teauxfu/py-hplc/actions/workflows/build.yml/badge.svg\n  :target: https://github.com/teauxfu/py-hplc/actions/workflows/build.yml\n  :alt: Build Status\n\n.. |docs| image:: https://readthedocs.org/projects/pip/badge/?version=stable\n  :target: https://py-hplc.readthedocs.io/en/latest/\n  :alt: Documentation Status\n\n.. |style| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n  :target: https://github.com/psf/black\n  :alt: Style\n  \n.. |pylint| image:: https://mperlet.github.io/pybadge/badges/9.87.svg\n  :target: https://github.com/mperlet/pybadge\n  :alt: Vanilla Pylint Score\n  \n',
    'author': 'Alex W',
    'author_email': 'alex@southsun.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/teauxfu/py-hplc',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

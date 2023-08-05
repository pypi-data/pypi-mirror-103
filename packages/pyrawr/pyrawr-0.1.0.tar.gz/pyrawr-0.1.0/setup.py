# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyrawr']
install_requires = \
['semver>=2']

setup_kwargs = {
    'name': 'pyrawr',
    'version': '0.1.0',
    'description': 'Python wrapper around the ThermoRawFileParser command line interface',
    'long_description': '# pyrawr\n\n[![](https://flat.badgen.net/pypi/v/pyrawr?icon=pypi)](https://pypi.org/project/pyrawr)\n[![](https://flat.badgen.net/github/release/ralfg/pyrawr)](https://github.com/ralfg/pyrawr/releases)\n[![](https://flat.badgen.net/github/checks/ralfg/pyrawr/)](https://github.com/ralfg/pyrawr/actions)\n![](https://flat.badgen.net/github/last-commit/ralfg/pyrawr)\n![](https://flat.badgen.net/github/license/ralfg/pyrawr)\n\n\nPython wrapper around the\n[ThermoRawFileParser](https://github.com/compomics/ThermoRawFileParser)\ncommand line interface.\n\nThis Python module uses the ThermoRawFileParser CLI to retrieve general run metadata, specific spectra, or specific XICs, directly as Python lists and dictionaries from\nmass spectrometry raw files. Parsing raw files to other file formats is also supported.\n\n\n---\n\n\n## Installation\n\n- Install pyrawr with pip\n\n   ```sh\n   $ pip install pyrawr\n   ```\n\n- Install [ThermoRawFileParser](https://github.com/compomics/ThermoRawFileParser) or\nDocker.\n\nFor Docker, the current user must be\n[added to the Docker group](https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user),\nthat is, be callable as `docker run`, instead of `sudo docker run`.\n\n\n## Usage\n\nSee\n[full API documentation](https://pyrawr.readthedocs.io/en/latest/api.html)\nfor all pyrawr functionality.\n\n\nParse raw file to any supported output format:\n\n```python\n>>> from pyrawr import ThermoRawFileParser\n>>> trfp = ThermoRawFileParser(\n...     executable="thermorawfileparser",\n...     docker_image="quay.io/biocontainers/thermorawfileparser:1.3.3--ha8f3691_1"\n... )\n>>> trfp.parse("OR4_110719_OB_PAR14_sSCX_fr10.raw", output_format="mzml")\n```\n\n\nGet raw file metadata:\n\n```python\n>>> trfp.metadata("OR4_110719_OB_PAR14_sSCX_fr10.raw")\n{\'FileProperties\': [{\'accession\': \'NCIT:C47922\', \'cvLabel\': \'NCIT\' ... }]}\n```\n\n\nQuery a specific spectrum:\n\n```python\n>>> trfp.query("OR4_110719_OB_PAR14_sSCX_fr10.raw", "508,680")\n[{\'mzs\': [204.8467254638672,\n   262.4529113769531,\n   309.53961181640625,\n   ...\n```\n\n\nRetrieve one or more chromatograms based on a query:\n\n```python\n>>> trfp.xic(\n...     "OR4_110719_OB_PAR14_sSCX_fr10.raw",\n...     [{"mz":488.5384, "tolerance":10, "tolerance_unit":"ppm"}],\n... )\n{\'OutputMeta\': {\'base64\': False, \'timeunit\': \'minutes\'},\n \'Content\': [{\'Meta\': {\'MzStart\': 488.53351461600005,\n    \'MzEnd\': 488.543285384,\n    \'RtStart\': 0.007536666666666666,\n    \'RtEnd\': 179.99577166666666},\n   \'RetentionTimes\': [0.007536666666666666,\n    0.022771666666666666,\n    0.036936666666666666,\n    ...\n```\n\n## Contributing\n\nBugs, questions or suggestions? Feel free to post an issue in the\n[issue tracker](https://github.com/RalfG/pyrawr/issues/) or to make a pull\nrequest! See\n[Contributing.md](https://pyrawr.readthedocs.io/en/latest/contributing.html)\nfor more info.\n\nThis module currently uses Python\'s `subprocess.run()` to access ThermoRawFileParser.\nThere are probably much better methods that would directly access the\nThermoRawFileParser library, circumventing the CLI. Suggestions and PRs are always\nwelcome.\n\n\n## Changelog\n\nSee [Changelog](https://pyrawr.readthedocs.io/en/latest/changelog.html).\n',
    'author': 'Ralf Gabriels',
    'author_email': 'ralf@gabriels.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ralfg/pyrawr',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

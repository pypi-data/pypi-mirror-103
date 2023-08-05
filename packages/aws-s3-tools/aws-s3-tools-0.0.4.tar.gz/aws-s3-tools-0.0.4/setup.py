# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['s3_tools', 's3_tools.objects']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.51,<2.0.0', 'ujson>=4.0.1,<5.0.0']

extras_require = \
{'progress': ['rich>=10.1.0,<11.0.0']}

setup_kwargs = {
    'name': 'aws-s3-tools',
    'version': '0.0.4',
    'description': 'AWS S3 tools package',
    'long_description': '# AWS S3 Tools\n\n![MIT License](https://img.shields.io/pypi/l/aws-s3-tools)\n[![Test](https://github.com/FerrariDG/aws-s3-tools/actions/workflows/test.yml/badge.svg)](https://github.com/FerrariDG/aws-s3-tools/actions/workflows/test.yml)\n[![codecov](https://codecov.io/gh/FerrariDG/aws-s3-tools/branch/main/graph/badge.svg?token=YRM26tZexs)](https://codecov.io/gh/FerrariDG/aws-s3-tools)\n![Documentation Status](https://readthedocs.org/projects/aws-s3-tools/badge/?version=latest)\n![Package Version](https://img.shields.io/pypi/v/aws-s3-tools)\n![Python Version](https://img.shields.io/pypi/pyversions/aws-s3-tools)\n\nAWS S3 Tools is a Python package to make it easier to deal with S3 objects, where you can:\n\n- Check if S3 objects exist\n- List S3 bucket content\n- Read from S3 objects to Python variables\n- Write from Python variables to S3 objects\n- Upload from local files to S3\n- Download from S3 to local files\n- Delete S3 objects\n- Move S3 objects\n\nThe AWS authentication is done via boto3 package,\n[click here to know more about it](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).\n\n---\n\n## Installation\n\nYou can install AWS S3 Tools from PyPi with `pip` or your favorite package manager:\n\n    pip install aws-s3-tools\n\nAdd the ``-U`` switch to update to the current version, if AWS S3 Tools is already installed.\n\nIf you want to use the **progress bar** feature when downloading or uploading,\nyou need to install an extra dependency.\n\n    pip install aws-s3-tools[progress]\n\n---\n\n## Usage\n\n[The full documentation can be found here](https://aws-s3-tools.readthedocs.io/en/latest/index.html).\n\n```python\nfrom s3_tools import object_exists\n\nif object_exists("my-bucket", "s3-prefix/object.data"):\n    # Do magic\nelse:\n    print("Object not found")\n```\n\nExample to use the progress bar:\n\n```python\nfrom s3_tools import upload_folder_to_prefix\n\nresult = upload_folder_to_prefix(\n    bucket=\'daniel-ferrari\',\n    prefix=\'aws-s3-tools\',\n    search_str=\'*.py\',\n    threads=2,\n    folder=\'s3_tools\',\n    show_progress=True\n)\n```\n\nProgress bar when running the code above:\n\n![Progress bar gif](docs/source/demo.gif)\n\n---\n\n## Contributions\n\nAll contributions, bug reports, bug fixes, documentation improvements,\nenhancements and ideas are welcome.\n\nA detailed overview on how to contribute can be found in the\n[contributing guide](CONTRIBUTING.md)\non GitHub.\n\n---\n\n## Issues\n\nGo [here](https://github.com/FerrariDG/aws-s3-tools/issues) to submit feature\nrequests or bugfixes.\n\n---\n\n## License and Credits\n\n`AWS S3 Tools` is licensed under the [MIT license](LICENSE) and is written and\nmaintained by Daniel Ferrari ([@FerrariDG](https://github.com/FerrariDG)) and Carlos Alves ([@cmalves](https://github.com/cmalves))\n\n---\n\n## Acknowledgement\n\nThe idea from these functions come from an amazing team that I worked with. This repo is a refactor and documentation to make this public to everyone.\n\nMany thanks to:\n\n- [Anabela Nogueira](https://www.linkedin.com/in/abnogueira/)\n- [Carlos Alves](https://www.linkedin.com/in/carlosmalves/)\n- [João Machado](https://www.linkedin.com/in/machadojpf/)\n- [Renato Dantas](https://www.linkedin.com/in/renatomoura/)\n- [Ricardo Garcia](https://www.linkedin.com/in/ricardo-g-oliveira/)\n- [Tomás Osório](https://www.linkedin.com/in/tomas-osorio/)\n',
    'author': 'Daniel Ferrari',
    'author_email': None,
    'maintainer': 'Carlos Alves',
    'maintainer_email': None,
    'url': 'https://github.com/FerrariDG/aws-s3-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

# AWS S3 Tools

![MIT License](https://img.shields.io/pypi/l/aws-s3-tools)
[![Test](https://github.com/FerrariDG/aws-s3-tools/actions/workflows/test.yml/badge.svg)](https://github.com/FerrariDG/aws-s3-tools/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/FerrariDG/aws-s3-tools/branch/main/graph/badge.svg?token=YRM26tZexs)](https://codecov.io/gh/FerrariDG/aws-s3-tools)
![Documentation Status](https://readthedocs.org/projects/aws-s3-tools/badge/?version=latest)
![Package Version](https://img.shields.io/pypi/v/aws-s3-tools)
![Python Version](https://img.shields.io/pypi/pyversions/aws-s3-tools)

AWS S3 Tools is a Python package to make it easier to deal with S3 objects, where you can:

- Check if S3 objects exist
- List S3 bucket content
- Read from S3 objects to Python variables
- Write from Python variables to S3 objects
- Upload from local files to S3
- Download from S3 to local files
- Delete S3 objects
- Move S3 objects

The AWS authentication is done via boto3 package,
[click here to know more about it](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html).

---

## Installation

You can install AWS S3 Tools from PyPi with `pip` or your favorite package manager:

    pip install aws-s3-tools

Add the ``-U`` switch to update to the current version, if AWS S3 Tools is already installed.

If you want to use the **progress bar** feature when downloading or uploading,
you need to install an extra dependency.

    pip install aws-s3-tools[progress]

---

## Usage

[The full documentation can be found here](https://aws-s3-tools.readthedocs.io/en/latest/index.html).

```python
from s3_tools import object_exists

if object_exists("my-bucket", "s3-prefix/object.data"):
    # Do magic
else:
    print("Object not found")
```

Example to use the progress bar:

```python
from s3_tools import upload_folder_to_prefix

result = upload_folder_to_prefix(
    bucket='daniel-ferrari',
    prefix='aws-s3-tools',
    search_str='*.py',
    threads=2,
    folder='s3_tools',
    show_progress=True
)
```

Progress bar when running the code above:

![Progress bar gif](docs/source/demo.gif)

---

## Contributions

All contributions, bug reports, bug fixes, documentation improvements,
enhancements and ideas are welcome.

A detailed overview on how to contribute can be found in the
[contributing guide](CONTRIBUTING.md)
on GitHub.

---

## Issues

Go [here](https://github.com/FerrariDG/aws-s3-tools/issues) to submit feature
requests or bugfixes.

---

## License and Credits

`AWS S3 Tools` is licensed under the [MIT license](LICENSE) and is written and
maintained by Daniel Ferrari ([@FerrariDG](https://github.com/FerrariDG)) and Carlos Alves ([@cmalves](https://github.com/cmalves))

---

## Acknowledgement

The idea from these functions come from an amazing team that I worked with. This repo is a refactor and documentation to make this public to everyone.

Many thanks to:

- [Anabela Nogueira](https://www.linkedin.com/in/abnogueira/)
- [Carlos Alves](https://www.linkedin.com/in/carlosmalves/)
- [João Machado](https://www.linkedin.com/in/machadojpf/)
- [Renato Dantas](https://www.linkedin.com/in/renatomoura/)
- [Ricardo Garcia](https://www.linkedin.com/in/ricardo-g-oliveira/)
- [Tomás Osório](https://www.linkedin.com/in/tomas-osorio/)

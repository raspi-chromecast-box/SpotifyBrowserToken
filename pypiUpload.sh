#!/bin/bash

#upload to pypi in 2020

#create ~/.pypirc
#[server-login]
#username:
#password:

# https://github.com/pypa/setuptools/issues/941#issuecomment-538353624

rm -rf build
rm -rf dist
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
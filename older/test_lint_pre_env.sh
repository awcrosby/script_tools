#!/bin/bash

echo 'Creates environment and installs ansible-lint alpha pre-release'

mkdir test_lint_pre
cd test_lint_pre

virtualenv venv --no-site-packages -p /usr/bin/python2.7
source venv/bin/activate

pip install ansible

## pypi dev release
pip install --pre -i https://test.pypi.org/simple/ ansible-lint

## pypi prod alpha release
# pip install --pre ansible-lint

## pypi prod latest release
# pip install ansible-lint

ansible-lint --version

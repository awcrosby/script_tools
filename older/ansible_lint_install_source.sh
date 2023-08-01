#!/bin/bash

echo 'Installs ansible-lint from source'
echo 'Run from location that contains the `ansible-lint` dir'

export PYTHONPATH=$PYTHONPATH:`pwd`/ansible-lint/lib
export PATH=$PATH:`pwd`/ansible-lint/bin

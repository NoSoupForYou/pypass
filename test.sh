#!/usr/bin/env bash

PYTHON="$( which python2 )"
time $PYTHON -c "import pypass; pypass.main()"

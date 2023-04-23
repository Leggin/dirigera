#!/bin/bash

source venv/bin/activate
python3 -m pylint $(git ls-files '*.py')
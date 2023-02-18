#!/bin/bash

set -a
source .env
source venv/bin/activate
python3 -m pytest .
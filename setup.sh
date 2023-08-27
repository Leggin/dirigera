#!/usr/bin/env bash

python3 -m venv venv

if [ "$(uname)" == "Darwin" ]; then
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    source venv/Scripts/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    source venv/Scripts/activate
fi

pip install -r requirements.txt
pip install -r dev-requirements.txt

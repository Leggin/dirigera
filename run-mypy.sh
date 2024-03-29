#!/usr/bin/env bash
set -a
source .env

if [ "$(uname)" == "Darwin" ]; then
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    source venv/bin/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    source venv/Scripts/activate
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    source venv/Scripts/activate
fi

mypy .

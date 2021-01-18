#!/bin/bash

if [ -d venv ]; then
  . venv/bin/activate
fi

python3 -m unittest discover

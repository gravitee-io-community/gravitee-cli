#!/bin/sh

BASH_PATH="`dirname \"$0\"`"

if [ -z "$BASH_PATH" ] ; then
  exit 1  # fail
fi

cd $BASH_PATH
cd ..

python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

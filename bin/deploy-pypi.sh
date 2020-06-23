#!/bin/sh

BASH_PATH="`dirname \"$0\"`"

if [ -z "$BASH_PATH" ] ; then
  exit 1  # fail
fi

cd $BASH_PATH
cd ..

# -e MYVAR1
python3 -m twine upload dist/*
docker run -it --rm python:3.8.3-alpine3.11 /bin/sh
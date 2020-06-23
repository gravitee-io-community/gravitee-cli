#!/bin/sh

BASH_PATH="`dirname \"$0\"`"

if [ -z "$BASH_PATH" ] ; then
  exit 1  # fail
fi

cd $BASH_PATH
cd ..
source .venv/bin/activate
python3 -m graviteeio_cli $@
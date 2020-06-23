#!/bin/sh

BASH_PATH="`dirname \"$0\"`"

if [ -z "$BASH_PATH" ] ; then
  exit 1  # fail
fi

cd $BASH_PATH
cd ..

rm -r dist/
sudo python3 -m pip install --upgrade setuptools wheel
python3 setup.py bdist_wheel
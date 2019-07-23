#!/bin/sh

pkill massivemacro_linux

rm -rf build dist Pipfile.lock

pipenv install --dev
pipenv run pyinstaller massivemacro_pyinstaller.spec

# This is for macos/build_without_pipenv.sh to use
pipenv lock -r > requirements.txt

mkdir -p bin
mv dist/massivemacro bin/massivemacro_linux

rm -rf build dist

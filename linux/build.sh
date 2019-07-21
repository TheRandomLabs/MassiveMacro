#!/bin/sh

pkill massivemacro_linux

rm -rf build dist Pipfile.lock

pipenv install --dev
pipenv run pyinstaller massivemacro_pyinstaller.spec

mkdir -p bin
mv dist/massivemacro bin/massivemacro_linux

rm -rf build dist

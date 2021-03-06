#!/bin/sh

pkill massivemacro
pkill massivemacro_macos

rm -rf build dist Pipfile.lock

pipenv install --dev
pipenv run pyinstaller massivemacro_pyinstaller.spec

mkdir -p bin
rm -rf bin/MassiveMacro.app
mv dist/massivemacro bin/massivemacro_macos
mv dist/MassiveMacro.app bin

platypus -P bin/MassiveMacro.platypus bin/MassiveMacro.app -y

codesign -s "MassiveMacro" bin/MassiveMacro.app

sh bin/platypus.sh

rm bin/MassiveMacro.zip
zip -r0 bin/MassiveMacro.zip bin/MassiveMacro.app

rm -rf build dist Info.plist

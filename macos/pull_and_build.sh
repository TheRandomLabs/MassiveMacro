#!/bin/sh

git fetch --all
git reset --hard origin/master
git pull

sh macos/build.sh

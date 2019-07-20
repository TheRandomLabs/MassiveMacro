@echo off

git fetch --all
git reset --hard origin/master
git pull

call windows\build.bat

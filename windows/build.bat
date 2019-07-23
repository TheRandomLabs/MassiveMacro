@echo off

taskkill /f /im MassiveMacro.exe

rmdir /q /s build
rmdir /q /s dist

del Pipfile.lock

pipenv install --dev
pipenv run pyinstaller massivemacro_pyinstaller.spec --version-file windows\version_info.txt

mkdir bin
move /y dist\massivemacro.exe bin\MassiveMacro.exe

rmdir /q /s build
rmdir /q /s dist

call windows\sign_private.bat

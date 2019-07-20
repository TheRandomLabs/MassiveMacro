# MassiveMacro

Massive text for Discord with the power of [massive.py](https://github.com/TheRandomLabs/massive.py).

## Building

Python 3.7 and Pipenv are required to run and build MassiveMacro.

Compiled executables are located in the `bin` directory.

### Windows

`build.bat` compiles an executable for Windows, and for Linux if WSL
(Windows Subsystem for Linux) is installed, called `MassiveMacro.exe` and `massivemacro_linux`
respectively.

`linux\build.bat` can be called from the root MassiveMacro directory to only compile an
executable for Windows.

`windows\build.bat` can be called from the root MassiveMacro directory to only compile an
executable for Windows.

`windows\pull_and_build.bat` pulls the latest version of MassiveMacro from GitHub before calling
`windows\build.bat`.

If `signtool` from the
[Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk)
is installed, `windows\sign_private.bat` is automatically called to sign the executable.
`windows\sign_private.bat` can be written like so:

```batch
@echo off
call windows\sign.bat %PFX_FILE% %PASSWORD%
```

### Linux

`sh linux/build.sh` can be run from the root MassiveMacro directory to compile a Linux executable.
The compiled executable is called `massivemacro_linux`.

`sh linux/pull_and_build.sh` can be run from the root MassiveMacro directory to pull the latest
version of MassiveMacro from GitHub before running `linux/build.sh`.

## Mac OS X

`sh macos/build.sh` can be run from the root MassiveMacro directory to compile a Mac OS X
executable. The script generates an executable called `massivemacro_macos`, a `.app` called
`MassiveMacro.app` and an archive that contains `MassiveMacro.app` called `MassiveMacro.zip`.

`sh macos/pull_and_build.sh` can be run from the root MassiveMacro directory to pull the latest
version of MassiveMacro from GitHub before running `macos/build.sh`.

## Usage

MassiveMacro is primarily built for Discord, but it works in other applications as well to varying
degrees. Vanessa text works flawlessly on other instant messaging platforms such as Skype and Steam.

Precompiled binaries are available for Windows, Linux and Mac OS X.

### Key bindings

    Ctrl+Enter: Plain massive (primarily regional indicators)
    Ctrl+Shift+Enter: Alternate massive (regional indicators mixed with alternate emojis)
    Alt+Shift+Enter: Vanessa (aLtErNaTe CaPs)
    Ctrl+Space+Enter: Massive Vanessa (combination of lowercase text and alternate massive)

Alternate Vanessa text will cause random words to be misspelled.

Multiple messages can be sent at once on Discord by typing multiple lines in the same message by
pressing `Shift+Enter` then using one of the above key bindings.

### Linux

On Linux, MassiveMacro requires `xsel` to be
installed:

    $ sudo apt install xsel

# MassiveMacro

Massive text for Discord with the power of [massive.py](https://github.com/TheRandomLabs/massive.py).

## Running and building

Python 3.7 and Pipenv are required to run and build MassiveMacro.

To run MassiveMacro directly:

	$ pipenv install
	$ pipenv run python run.py

Compiled executables are located in the `bin` directory:

### Windows

`build.bat` compiles an executable for Windows, and for Linux if WSL
(Windows Subsystem for Linux) is installed, called `MassiveMacro.exe` and `massivemacro_linux`
respectively.

`linux\build.bat` can be called from the root MassiveMacro directory to only compile an
executable for Linux if WSL is installed.

Building a Linux executable on WSL requires `qt5-default` to be installed. An executable built on
WSL displays Fontconfig errors in the terminal when run, but otherwise functions normally.

`windows\build.bat` can be called from the root MassiveMacro directory to only compile an
executable for Windows.

`windows\pull_and_build.bat` pulls the latest version of MassiveMacro from GitHub before calling
`windows\build.bat`.

If `signtool` from the
[Windows 10 SDK](https://developer.microsoft.com/en-us/windows/downloads/windows-10-sdk)
is installed, `windows\sign_private.bat` is automatically called to sign the executable.

`signtool` can also be installed by installing `windows-sdk-signing-tools` from
[here](https://github.com/TheRandomLabs/Scoop-Bucket) using
[Scoop](https://github.com/lukesampson/scoop).

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

### macOS

`sh macos/build.sh` can be run from the root MassiveMacro directory to compile a macOS
executable. The script generates an executable called `massivemacro_macos`, a `.app` called
`MassiveMacro.app` and an archive that contains `MassiveMacro.app` called `MassiveMacro.zip`.

`macos/build.sh` signs the `.app` with the `"MassiveMacro"` certificate by default.

`sh macos/pull_and_build.sh` can be run from the root MassiveMacro directory to pull the latest
version of MassiveMacro from GitHub before running `macos/build.sh`.

If the `.app` file does not open, [Platypus](https://sveinbjorn.org/platypus) should be used with
the `.app` file being added to the bundled files and the script written as such:

```bash
#!/bin/bash
./MassiveMacro.app/Contents/MacOS/massivemacro
```

If there is a Platypus profile at `bin/MassiveMacro.platypus`, it is automatically executed when
`macos/build.sh` is run.

## Usage

MassiveMacro is primarily built for Discord, but it works in other applications as well to varying
degrees. Vanessa text works flawlessly on other instant messaging platforms such as Skype and Steam.

Messages longer than 2000 characters (Discord's character limit) are automatically split into
multiple messages by default.

The command line option `--no-gui` can be used to disable the GUI.

Precompiled binaries are available for Windows, Linux and macOS 10.13+.

### Key bindings

Default key bindings:

![](https://raw.githubusercontent.com/TheRandomLabs/MassiveMacro/master/key_bindings.png)

Massive Vanessa text causes random words to be misspelled.

Multiple messages can be sent at once on Discord by typing multiple lines in the same message by
pressing `Shift+Enter` then using one of the above key bindings.

### Linux

On Linux, MassiveMacro requires `xsel` to be
installed:

	$ sudo apt install xsel

When the GUI is enabled, Qt 5 is also required:

	$ sudo apt install qt5-default

Additionally, MassiveMacro is built against glibc 2.23, which means it only runs with glibc 2.23
or newer.

### macOS

MassiveMacro needs either root or
[accessibility permissions](https://mizage.com/help/accessibility.html). To use the `.app`,
whitelist the `.app`. Otherwise, whitelist the terminal.

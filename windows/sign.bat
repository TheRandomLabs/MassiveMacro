@echo off
signtool sign /v /f %1 /p %2 /t http://timestamp.verisign.com/scripts/timstamp.dll bin\MassiveMacro.exe

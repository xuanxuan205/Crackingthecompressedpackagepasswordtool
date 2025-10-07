@echo off
REM 一键打包并运行 密码破解工具

set MAIN=main.py
set ICON=icon.ico
set VERSION=version.txt
set EXENAME=密码破解工具.exe

pyinstaller -F -w --icon=%ICON% --version-file=%VERSION% --name "%EXENAME:~0,-4%" %MAIN%

cd dist
start "" "%EXENAME%"
cd ..

pause 
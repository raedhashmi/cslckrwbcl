@echo off

for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "Blue=%ESC%[34m"
set "Reset=%ESC%[0m"
set "Bold=%ESC%[1m"

setlocal enabledelayedexpansion

set /p create_main="%Blue%?%Reset% %Bold%Create main program? (Y/N): %Reset%"
set /p create_updater="%Blue%?%Reset% %Bold%Create updater? (Y/N): %Reset%"
set /p upload="%Blue%?%Reset% %Bold%Upload to server and change version? (Y/N): %Reset%"

if /i "!create_main!"=="Y" (
    .venv_main\Scripts\pyinstaller.exe --clean .\cslckrwbcl.spec --workpath ../cslckrwbcl-builds --distpath output
)
if /i "!create_updater!"=="Y" (
    .venv_updater\Scripts\pyinstaller.exe --clean --onefile --noconsole "./cslckrwbcl updater.py" --name="cslckrwbcl updater" --icon="favicon.ico" --workpath ../cslckrwbcl-builds --distpath output/updater
    del /f /q "cslckrwbcl updater.spec"
)
if /i "!upload!"=="Y" (
    echo %Blue%^^!%Reset% %Bold%SCPing the files to the server%Reset%
    scp "output/cslckrwbcl.exe" root@168.231.109.58:/root/cslckr/templates/
    scp "output/updater/cslckrwbcl updater.exe" root@168.231.109.58:/root/cslckr/templates/
    scp "version.txt" root@168.231.109.58:/root/cslckr/templates/
    echo %Blue%^^!%Reset% %Bold%Compiled successfuly.%Reset%

    echo %Blue%^^!%Reset% %Bold%Updating version.txt%Reset%
    python "update version.py"
)

exit /b
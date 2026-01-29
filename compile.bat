@echo off

for /F %%a in ('echo prompt $E ^| cmd') do set "ESC=%%a"

set "Blue=%ESC%[34m"
set "Reset=%ESC%[0m"
set "Bold=%ESC%[1m"

setlocal enabledelayedexpansion

set /p create_main="%Blue%?%Reset% %Bold%Create main program? (Y/N): %Reset%"
set /p create_updater="%Blue%?%Reset% %Bold%Create updater? (Y/N): %Reset%"

if /i "!create_main!"=="Y" (
    del /s /q /f "screen_recordings\*.*"
    for /d %%i in ("screen_recordings\*") do rd /s /q "%%i"
    pyinstaller --workpath ../cslckrwbcl-builds --distpath output .\cslckrwbcl.spec --clean --upx-dir="C:\Users\raedh\AppData\Local\Microsoft\WinGet\Packages\UPX.UPX_Microsoft.Winget.Source_8wekyb3d8bbwe\upx-5.1.0-win64\"
)
if /i "!create_updater!"=="Y" (
    pyinstaller --clean --onefile --noconsole "cslckrwbcl updater.py" --name="cslckrwbcl updater" --icon="favicon.ico" --workpath ../cslckrwbcl-builds --distpath output/updater --upx-dir="C:\Users\raedh\AppData\Local\Microsoft\WinGet\Packages\UPX.UPX_Microsoft.Winget.Source_8wekyb3d8bbwe\upx-5.1.0-win64\"
)

del /f /q "cslckrwbcl updater.spec"
echo %Blue%^^!%Reset% %Bold%SCPing the files to the server%Reset%
echo %Blue%This is the public version and so the files on the server cannot be modified. Keep this local by changing all the links in updater and main py file from cslckrmngr.lrdevstudio.com to something like localhost:3000 pointing to a folder.%Reset%
echo %Blue%^^!%Reset% %Bold%Compiled successfuly.%Reset%
exit /b
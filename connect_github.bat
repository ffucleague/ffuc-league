@echo off
title Connect FFUC to GitHub
echo ===================================================
echo   CONNECTING FFUC_WEBSITE TO GITHUB (ffucleague)
echo ===================================================
echo.
echo Step 1: Authorizing GitHub account 'ffucleague'...
echo.
echo A one-time code will be displayed below and your browser
echo will open to https://github.com/login/device.
echo Simply enter the code and click 'Authorize github'.
echo.
"C:\Program Files\GitHub CLI\gh.exe" auth login --web -p https
echo.
if %errorlevel% neq 0 (
    echo [ERROR] GitHub authorization was not completed.
    pause
    exit /b %errorlevel%
)
echo.
echo Step 2: Creating repository 'ffuc-league' and pushing website code...
echo.
cd /d "C:\Users\Mark Borrego\Desktop\FFUC_Website"
"C:\Program Files\GitHub CLI\gh.exe" repo create ffucleague/ffuc-league --public --source="C:\Users\Mark Borrego\Desktop\FFUC_Website" --remote=origin --push
echo.
if %errorlevel% equ 0 (
    echo ===================================================
    echo [SUCCESS] Your repository is live at:
    echo   https://github.com/ffucleague/ffuc-league
    echo ===================================================
) else (
    echo If repository already existed, setting remote and pushing...
    "C:\Program Files\Git\cmd\git.exe" remote add origin https://github.com/ffucleague/ffuc-league.git 2>nul
    "C:\Program Files\Git\cmd\git.exe" push -u origin main
)
echo.
echo You can now connect this repository to your Netlify site for 100% automated deploys!
pause

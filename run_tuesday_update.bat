@echo off
title F.F.U.C. Weekly Tuesday Automation
echo ===================================================
echo   F.F.U.C. FANTASY LEAGUE AUTOMATION BOT
echo ===================================================
echo Fetching Sleeper stats, recalculating standings,
echo and updating ffucleague.com...
echo.

python "%~dp0automated_update.py"

echo.
echo ===================================================
echo Done! Window will close in 10 seconds.
timeout /t 10 >nul

@echo off
title Setup F.F.U.C. Tuesday Automation Task
echo ===================================================
echo   REGISTERING TUESDAY 11:00 AM SCHEDULED TASK
echo ===================================================
echo.

schtasks /create /tn "FFUC_Weekly_Automation" /tr "\"%~dp0run_tuesday_update.bat\"" /sc weekly /d TUE /st 11:00 /f

echo.
if %errorlevel% equ 0 (
    echo [SUCCESS] Windows Task successfully scheduled!
    echo It will run automatically every Tuesday at 11:00 AM CST.
) else (
    echo [NOTE] If you got an "Access is denied" error, right-click
    echo "setup_scheduled_task.bat" and select "Run as administrator".
)
echo.
pause

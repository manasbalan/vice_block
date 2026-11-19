@echo off
title VICE CITY BLOCKS - Low-Spec GTA 6
echo Launching Vice City Blocks...
python server.py
if %ERRORLEVEL% NEQ 0 (
    echo Python server failed to start, opening directly in browser...
    start index.html
)
pause

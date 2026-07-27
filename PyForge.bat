@echo off
rem Double-click this to start PyForge.
rem Uses pythonw so no console window hangs around behind the app.
cd /d "%~dp0"
start "" pythonw app.py
if errorlevel 1 (
    echo pythonw not found - falling back to python
    python app.py
    pause
)

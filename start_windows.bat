@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating environment...
  py -3 -m venv .venv
  if errorlevel 1 goto error
)
echo [2/3] Installing dependencies...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
echo [3/3] Starting app: http://127.0.0.1:5000
".venv\Scripts\python.exe" app.py
pause
exit /b 0
:error
echo ERROR: Check Python installation and your Internet connection.
pause
exit /b 1

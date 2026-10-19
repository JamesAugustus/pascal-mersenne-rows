@echo off
where py >nul 2>&1
if errorlevel 1 goto use_python
py -3 "%~dp0install.py" %*
exit /b %errorlevel%
:use_python
python "%~dp0install.py" %*
exit /b %errorlevel%

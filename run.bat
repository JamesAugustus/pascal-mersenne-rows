@echo off
where py >nul 2>&1
if errorlevel 1 goto use_python
py -3 "%~dp0mersenne_rows.py" %*
exit /b %errorlevel%
:use_python
python "%~dp0mersenne_rows.py" %*
exit /b %errorlevel%

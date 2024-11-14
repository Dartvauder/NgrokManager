@echo off

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate
python -m pip install --upgrade pip setuptools
pip install wheel
pip install -r TechicalFiles/requirements.txt
timeout /t 2 /nobreak >nul
cls

echo Application installation process completed. Run start.bat to launch the application.

call venv\Scripts\deactivate.bat

pause
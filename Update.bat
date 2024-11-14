@echo off

git pull
timeout /t 2 /nobreak >nul
cls

call venv\Scripts\activate

echo Updating Application...
python -m pip install --upgrade pip setuptools
pip install wheel
pip install -r TechicalFiles/requirements.txt
timeout /t 2 /nobreak >nul
cls

echo Application updating process completed. Run start.bat to launch the application.

call venv\Scripts\deactivate.bat

pause

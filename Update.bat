@echo off

git pull

call venv\Scripts\activate

pip install -r requirements.txt

deactivate

#!/bin/bash

git pull
sleep 2
clear

echo "Updating Application..."
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools
pip install wheel
pip install -r TechnicalFiles/requirements.txt
sleep 2
clear

echo "Application updating process completed. Run start.sh to launch the application."

deactivate

read -p "Press enter to continue"

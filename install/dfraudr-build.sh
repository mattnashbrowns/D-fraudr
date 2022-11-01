#!/usr/bin/bash
cd /D-Fraudr
export PATH=$PATH:/home/dfraudr/.local/bin
echo pip -r requirements.txt
pip install -r requirements.txt
echo pip install dfraudr
pip install -e dfraudr
echo flask --app dfraudr init-db
flask --app dfraudr init-db
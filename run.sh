#!/usr/bin/bash
export PATH=$PATH:/home/dfraudr/.local/bin
cd /D-Fraudr

#"python3", "-m" , "flask", ?--app?, ?dfraudr?, "run", "--host=0.0.0.0"
#python3 -m flask --app dfraudr run --host=0.0.0.0
flask --app dfraudr --debug run --host=0.0.0.0
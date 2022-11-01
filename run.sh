#!/usr/bin/bash
cd /D-Fraudr
pipenv shell

#"python3", "-m" , "flask", ?--app?, ?dfraudr?, "run", "--host=0.0.0.0"
#python3 -m flask --app dfraudr run --host=0.0.0.0
flask --app dfraudr --debug run
#!/usr/bin/bash
export PATH=$PATH:/home/dfraudr/.local/bin
cd /D-Fraudr

flask --app dfraudr --debug run --host=0.0.0.0
#!/usr/bin/bash
echo Creating cluster
pg_createcluster 14 dfraudr --start --start-conf=auto

echo Configuring database server...
psql -f dfraudr/db-setup.sql

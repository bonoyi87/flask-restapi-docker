#!/usr/bin/env bash
db_host="db"  
db_port=3306

while ! nc $db_host $db_port; do  
  >&2 echo "DB is unavailable - sleeping"
  sleep 1
done

echo "Apply database migrations"  

pipenv run flask db upgrade
pipenv run python autoapp.py

#!/usr/bin/env bash

pipenv run flask db upgrade
pipenv run python autoapp.py

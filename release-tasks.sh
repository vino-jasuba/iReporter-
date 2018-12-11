#!/usr/bin/env bash

mv ./.env.example .env
source ./env/bin/activate
python ./manage.py -a

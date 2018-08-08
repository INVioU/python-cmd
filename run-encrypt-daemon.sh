#!/usr/bin/env bash

# NOTE: FIRST RUN "pipenv shell"
export FLASK_APP=daemon.py
export FLASK_DEBUG=1
flask run
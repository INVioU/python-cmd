#!/usr/bin/env bash

# TO RUN: "pipenv run ./run-encrypt-daemon.sh"
export FLASK_APP=daemon.py
export FLASK_DEBUG=1
flask run --port 8080
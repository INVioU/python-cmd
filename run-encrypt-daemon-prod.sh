#!/bin/bash

export FLASK_APP=daemon.py
export FLASK_DEBUG=1

flask run --host=0.0.0.0 --port 80

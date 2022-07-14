#!/bin/bash

python run.py
# gunicorn run:app -w 1 -b 0.0.0.0:5000 --timeout=10 -k gevent --log-level=debug
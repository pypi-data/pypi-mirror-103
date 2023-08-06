#!/bin/bash
rm -rf ./venv/lib/python3.8/site-packages/flask_regiment*
cp -r ../flask_regiment ./venv/lib/python3.8/site-packages/
FLASK_APP=test_flask_regiment FLASK_RUN_PORT=12345 ./venv/bin/flask run
#!/bin/bash

cd /app

python3 server/manage.py migrate --no-input
python3 server/manage.py create_test_data

#!/bin/bash

# Vector Demonstration Intialization  
#

# Applying the migrations
# Generating client app
npm install --prefix client && npm run build --prefix client
pipenv install
pipenv run python server/manage.py makemigrations && pipenv run python server/manage.py migrate 
pipenv shell "server/runserver.sh"


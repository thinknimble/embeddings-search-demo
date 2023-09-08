##

#
# This file contains helpful shortcuts to common commands needed when using
# Docker and Docker Compose in development. It can also serve as a cheat-
# sheet and documentation of the commands.
#
# Example: build and run all docker containers for development
#
#   make build
#   make run
#
# This will start all of the docker containers in 'detached' mode (that is,
# running in the background).
#
# Look at the logs:
#
#   make logs
#
# Example: You are a front-end developer who does not need a server
#
#   make build-client
#   make run-client
#
# These commands build and start running the client container. When they
# are done, you should be able to visit localhost:8080 in your browser and
# see the running Vue app.
#
# You may wish to run commands inside of the container. For example, you
# need to do this to install a new npm package:
#
#	make client-shell
#
# This will place you inside of the container in the /app/client directory
# where you can run `npm install {package_name}` as usual.
##


build:
	docker compose build

build-client:
	docker compose build client

build-server:
	docker-compose build server

run:
	docker compose up

run-client:
	docker compose up client

run-server:
	docker compose up server

run-d:
	docker compose up -d

run-client-d:
	docker compose up client -d

run-server-d:
	docker compose up server -d

restart:
	docker compose down && docker-compose up

client-shell:
	docker compose run client sh

server-shell:
	docker compose run server bash

create-test-data:
	docker compose run server python server/manage.py create_test_data

logs:
	docker compose logs -f

clean-all: clean clean-volumes

clean:
	docker compose down --rmi all

clean-volumes:
	docker compose down -v

commands:
	"$$0" -c "grep -E '^(\s*$|#)' './Makefile'"


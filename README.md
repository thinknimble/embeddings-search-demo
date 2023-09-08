[![Built with Cookiecutter](https://img.shields.io/badge/built%20with-Cookiecutter-ff69b4.svg?logo=cookiecutter)](https://github.com/thinknimble/tn-spa-bootstrapper)

# Vector Demonstration

A lot of people have asked us for ideas of how they can leverage Large Language Models (LLMs) for their business applications. A common example is to use the native language comprehension capabilities of LLMs to find matching content. This makes LLMs an excellent tool for search!

This repo demonstrates a prototype application that enables searching for job descriptions using an unstructured, English-language description of a job seeker.

[![Video: How We're Building AI Search Engines using LLM Embeddings](http://img.youtube.com/vi/ZCPUmC37HLU/0.jpg)](http://www.youtube.com/watch?v=ZCPUmC37HLU "How We're Building AI Search Engines using LLM Embeddings")

## Setup

### Docker

If this is your first time...

1. [Install Docker](https://www.docker.com/)
1. Run `pipenv lock` to generate a Pipfile.lock
1. Run `cd client && npm install` so you have node_modules available outside of Docker
1. Back in the root directory, run `make build`
1. `make run` to start the app
1. If the DB is new, run `make create-test-data`
   1. SuperUser `admin@thinknimble.com` with credentials from your `.env`
   1. User `cypress@thinknimble.com` with credentials from your `.env` is used by the Cypress
      tests
1. View other available scripts/commands with `make commands`
1. `localhost:8080` to view the app.
1. `localhost:8000/staff/` to log into the Django admin
1. `localhost:8000/api/docs/` to view backend API endpoints available for frontend development

### Backend

If not using Docker...
See the [backend README](server/README.md)

### Frontend

If not using Docker...
See the [frontend README](client/README.md)

## Testing & Linting Locally

1. `pipenv install --dev`
1. `pipenv run pytest server`
1. `pipenv run black server`
1. `pipenv run isort server --diff` (shows you what isort is expecting)
1. `npm run cypress`

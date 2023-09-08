#
# Define the 'web' process to be run on Heroku
#
web: gunicorn vector_demonstration.wsgi --chdir=server --log-file -

#
# This is not mandatory for all projects, as our process currently utilizes long-term staging
# servers, and automatically running migrations on this staging server could cause issues when
# different feature branches have different migrations. The aim is to switch to a model where our
# staging servers have a smaller lifetime, and we would not run into the above issue.
# To make this switch the following problems need to be solved.
#   1. Setting up human-readable URLS for the short-lived staging servers.
#   2. Fixtures for common test data (ex: test users, common app-specific entities)
#   3. Up-to-date build numbers shown in app (ideally auto-generated at build-and-deploy time)
#
# Comment the line below to disable migrations automatically after a Heroku push.
release: python server/manage.py migrate --noinput



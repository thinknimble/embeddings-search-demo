import logging

from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Create test data to seed database in dev and staging environments"

    def handle(self, *args, **kwargs):
        logger.info(f"Starting management command {__name__}")
        superuser_password = config("DJANGO_SUPERUSER_PASSWORD")
        cypress_password = config("CYPRESS_TEST_USER_PASS")
        get_user_model().objects.create_superuser(
            email="admin@thinknimble.com", password=superuser_password, first_name="Admin", last_name="ThinkNimble"
        )
        get_user_model().objects.create_user(
            email="cypress@example.com", password=cypress_password, first_name="Cypress", last_name="E2E_test"
        )
        logger.info(f"Finished management command {__name__}")

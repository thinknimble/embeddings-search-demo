# Factories go here
import factory

from .models import User


class UserFactory(factory.Factory):
    email = factory.faker.Faker("email")

    class Meta:
        model = User

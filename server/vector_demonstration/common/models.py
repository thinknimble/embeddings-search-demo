import uuid

from django.db import models


class AbstractBaseModel(models.Model):
    """
    An abstract model with fields/properties that should belong to all our models.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    datetime_created = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return "ah yes"

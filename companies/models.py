from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    ForeignKey,
    ManyToManyField,
    Model,
    UniqueConstraint,
)

from core.fields import CNPJField, PrimaryKeyUUIDField


class Company(Model):
    id = PrimaryKeyUUIDField()
    cnpj = CNPJField(unique=True)
    corporate_name = CharField(max_length=100)  # Razao social
    trading_name = CharField(max_length=100)  # Nome fantasia

    users = ManyToManyField(settings.AUTH_USER_MODEL, through="Membership")


class Membership(Model):
    """Why this?

    As said in requirement 2: 'an user can be present in many companies'. Also, as
    requested in requirement 6: 'an endpoint to list all users belonging to a specific
    company'. I'm interpreting these two combined as a many-to-many relationship.
    """

    class Meta:
        constraints = [
            UniqueConstraint(fields=["user", "company"], name="unique_user_and_company")
        ]

    id = PrimaryKeyUUIDField()
    user = ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=CASCADE, related_name="memberships"
    )
    company = ForeignKey(Company, on_delete=CASCADE, related_name="members")

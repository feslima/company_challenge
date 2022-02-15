import django.utils.timezone
from django.conf import settings
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    UniqueConstraint,
)

from core.fields import CNPJField, PrimaryKeyUUIDField


class Company(Model):
    id = PrimaryKeyUUIDField()
    cnpj = CNPJField(unique=True)
    company_name = CharField(max_length=100, help_text="Also known as 'Razão Social'.")
    commercial_name = CharField(
        max_length=100, help_text="Also known as 'Nome fantasia'."
    )
    created = DateTimeField(
        "created", auto_now_add=True, help_text="When the company was created."
    )
    last_update = DateTimeField(
        "last update",
        default=django.utils.timezone.now,
        help_text="Last time this company was synchronized against receitaws.",
    )

    users = ManyToManyField(
        settings.AUTH_USER_MODEL, through="Membership", related_name="companies"
    )


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

    date_joined = DateTimeField(
        "date joined", auto_now_add=True, help_text="When the user joined the company."
    )

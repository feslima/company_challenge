from __future__ import annotations

from typing import Generic, TypeVar

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db.models import BooleanField, CharField, DateTimeField, EmailField

from core.fields import PrimaryKeyUUIDField

T = TypeVar("T", bound="CompanyUser", covariant=True)


class CompanyUserManager(Generic[T], BaseUserManager[T]):
    def create_user(
        self, email: str, first_name: str, surname: str, password: str
    ) -> T:
        email = self.normalize_email(email)

        user = self.model(email=email, first_name=first_name, surname=surname)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, email: str, first_name: str, surname: str, password: str
    ) -> T:
        user = self.create_user(email, first_name, surname, password)
        user.is_active = True
        user.staff = True

        user.save(using=self._db)
        return user


class CompanyUser(AbstractBaseUser, PermissionsMixin):
    """Custom user definition for the application to use email as the username.

    Whenever you create a new user, make sure to call `create_user` instead
    of `create`. Otherwise the password is not going to be hashed.
    """

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    id = PrimaryKeyUUIDField()
    email = EmailField("user email", unique=True)
    first_name = CharField(
        "first name",
        max_length=50,
        help_text="User's first name.",
    )
    surname = CharField(
        "surname name",
        max_length=100,
        help_text="User's surname.",
    )
    date_joined = DateTimeField("date joined", auto_now_add=True)
    is_active = BooleanField("active", default=True)
    staff = BooleanField(
        "staff status",
        default=False,
        help_text="Whether user is allowed on admin site or not.",
    )

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "surname"]

    objects = CompanyUserManager()

    @property
    def full_name(self) -> str:
        """User's full name"""
        return f"{self.first_name} {self.surname}"

    def __str__(self) -> str:
        return f"{self.full_name} ({self.email})"

    @property
    def is_staff(self):
        "Is this user a staff member?"
        return self.staff

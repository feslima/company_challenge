from typing import Any, Dict

from django.contrib.auth import authenticate, login
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as CoreValidationError
from rest_framework.serializers import (
    CharField,
    EmailField,
    ModelSerializer,
    Serializer,
    ValidationError,
)

from .models import CompanyUser


class CompanyUserSerializer(ModelSerializer):
    class Meta:
        model = CompanyUser
        fields = (
            "email",
            "first_name",
            "surname",
            "password",
            "email_confirm",
            "password_confirm",
        )
        extra_kwargs = {
            "email": {"help_text": "User's email."},
            "password": {"write_only": True, "help_text": "User's password."},
        }

    email_confirm = EmailField(write_only=True, help_text="Confirm email address.")
    password_confirm = CharField(write_only=True, help_text="Confirm password.")

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:

        first_name = data["first_name"]
        surname = data["surname"]
        email = data["email"]
        email_confirm = data["email_confirm"]
        password = data["password"]
        password_confirm = data["password_confirm"]

        # email check
        if email != email_confirm:
            msg = "Emails don't match."
            raise ValidationError(
                {"email": msg, "email_confirm": msg}, code="emails_not_mach"
            )

        # password validation
        if password != password_confirm:
            msg = "Passwords don't match."
            raise ValidationError(
                {"password": msg, "password_confirm": msg},
                code="passwords_not_match",
            )

        user = CompanyUser(
            email=email, first_name=first_name, surname=surname, password=password
        )
        try:
            validate_password(password, user)
        except CoreValidationError as ex:
            msg = ex.message
            raise ValidationError(
                {"password": msg, "password_confirm": msg}, code="invalid_passwords"
            )

        return data

    def create(self, validated_data: Dict[str, Any]) -> CompanyUser:
        email = validated_data["email"]
        first_name = validated_data["first_name"]
        surname = validated_data["surname"]
        password = validated_data["password"]

        user = CompanyUser.objects.create_user(
            email=email, first_name=first_name, surname=surname, password=password
        )
        return user


class LoginSerializer(Serializer):
    email = EmailField(help_text="User's email.")
    password = CharField(write_only=True, help_text="User's password.")

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, Any]:
        user = authenticate(username=attrs["email"], password=attrs["password"])
        if user is None:
            msg = "Invalid credentials."
            raise ValidationError(
                {"email": msg, "password": msg}, code="invalid_credentials"
            )

        return {"user": user}

    def create(self, validated_data: Dict[str, CompanyUser]) -> Dict[str, str]:
        user = validated_data["user"]
        login(self.context["request"], user)
        return {"email": user.email}

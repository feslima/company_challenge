from typing import Any, Dict

from django.db.transaction import atomic
from rest_framework.serializers import (
    ModelSerializer,
    SlugRelatedField,
    ValidationError,
)
from rest_framework.validators import UniqueTogetherValidator

from users.models import CompanyUser

from .models import Company, Membership


def validate_user_exists(email: str) -> None:
    try:
        CompanyUser.objects.get(email=email)
    except CompanyUser.DoesNotExist:
        raise ValidationError("User not found.", code="user_not_found.")


class CompanyMemberCreationSerializer(ModelSerializer):
    """Serializer used only for when creating a company with an user associated by
    default."""

    class Meta:
        model = CompanyUser
        fields = ["email"]
        extra_kwargs = {
            "email": {"write_only": True, "validators": [validate_user_exists]}
        }


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ["cnpj", "corporate_name", "trading_name"]


class CompanyCreationSerializer(ModelSerializer):
    """Serializes the many to many Membership by requiring an already registered user
    identifier (email), at the moment the company is created."""

    user = SlugRelatedField(
        slug_field="email", many=False, queryset=CompanyUser.objects.all()
    )
    company = CompanySerializer()

    class Meta:
        model = Membership
        fields = ["user", "company"]

    def create(self, validated_data: Dict[str, Any]) -> Membership:
        with atomic():
            company: Company = Company(**validated_data["company"])
            company.full_clean()
            company.save()

            user: CompanyUser = validated_data["user"]

            membership: Membership = Membership(company=company, user=user)
            membership.full_clean()
            membership.save()

        return membership


class MembershipSerializer(ModelSerializer):
    class Meta:
        model = Membership
        fields = ["user", "company"]
        validators = [
            UniqueTogetherValidator(
                fields=["user", "company"],
                queryset=Membership.objects.all(),
                message="This user is already registered in this company.",
            )
        ]

    user = SlugRelatedField(
        slug_field="email", many=False, queryset=CompanyUser.objects.all()
    )
    company = SlugRelatedField(
        slug_field="cnpj", many=False, queryset=Company.objects.all()
    )

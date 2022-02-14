from typing import Any, Dict

import factory
import pytest
from faker import Faker

from companies.factories import CompanyFactory
from companies.models import Company, Membership
from companies.serializers import CompanyCreationSerializer
from users.factories import CompanyUserFactory
from users.models import CompanyUser


@pytest.fixture
def registered_user(user_data) -> CompanyUser:
    return CompanyUserFactory.create(**user_data)


@pytest.mark.django_db
def test_creation_serializer(
    company_data: Dict[str, Any], registered_user: CompanyUser
):
    data = {"company": company_data, "user": registered_user.email}
    serializer = CompanyCreationSerializer(data=data)

    assert serializer.is_valid(), serializer.errors

    membership: Membership = serializer.save()
    company: Company = membership.company
    assert company.users.count() == 1, "Company must have a single user when created"
    assert company.users.filter(email=registered_user.email).exists()


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_cnpj_uniqueness(company_data: Dict[str, Any], registered_user: CompanyUser):
    CompanyFactory.create(**company_data)

    data = {"company": company_data, "user": registered_user.email}
    serializer = CompanyCreationSerializer(data=data)

    assert not serializer.is_valid()
    assert "company" in serializer.errors
    assert "cnpj" in serializer.errors["company"]


@pytest.mark.django_db
def test_should_fail_when_providing_an_unregistered_user(
    company_data: Dict[str, Any], faker: Faker
):
    unregistered_email = faker.email()
    data = {"company": company_data, "user": unregistered_email}
    serializer = CompanyCreationSerializer(data=data)

    assert not serializer.is_valid()
    assert "user" in serializer.errors
    assert f"{unregistered_email} does not exist." in serializer.errors["user"][0]

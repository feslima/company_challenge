from random import choice
from typing import Any, Dict, List

import factory
import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.settings import api_settings
from rest_framework.test import APIClient

from companies.factories import CompanyFactory, MembershipFactory
from companies.models import Company, Membership
from users.factories import CompanyUserFactory
from users.models import CompanyUser


@pytest.mark.django_db
def test_company_creation(api_client: APIClient, company_data: Dict[str, Any]):
    # We need an already registered user on the moment the company is created
    user: CompanyUser = CompanyUserFactory.create()

    data = {"company": company_data, "user": user.email}

    url = reverse("companies:create")
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert Company.objects.filter(cnpj=company_data["cnpj"]).count() == 1


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_membership_creation(api_client: APIClient):
    # create a company with a single user
    membership: Membership = MembershipFactory.create()

    new_user: CompanyUser = CompanyUserFactory.create()
    cnpj = membership.company.cnpj
    data = {"company": cnpj, "user": new_user.email}
    url = reverse("companies:members:create", kwargs={"cnpj": cnpj})
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert Company.objects.filter(cnpj=cnpj).count() == 1
    assert Membership.objects.count() == 2
    assert Membership.objects.filter(user=new_user).count() == 1


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_membership_uniqueness(api_client: APIClient):
    membership: Membership = MembershipFactory.create()
    user: CompanyUser = membership.user
    cnpj = membership.company.cnpj

    data = {"company": cnpj, "user": user.email}
    url = reverse("companies:members:create", kwargs={"cnpj": cnpj})

    response = api_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.json()

    errors = response.data[api_settings.NON_FIELD_ERRORS_KEY]
    error_msg = "This user is already registered in this company."

    assert len(errors) == 1
    assert error_msg in errors[0]


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_retrieve_company_detail_by_cnpj(api_client: APIClient):
    companies: List[Company] = CompanyFactory.create_batch(4)
    company: Company = choice(companies)

    url = reverse("companies:detail", kwargs={"cnpj": company.cnpj})
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert "cnpj" in response.data
    assert response.data["cnpj"] == company.cnpj

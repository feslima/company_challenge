from typing import Any, Dict, List

import factory
import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from companies.factories import CompanyFactory, MembershipFactory
from companies.models import Company, Membership
from users.factories import CompanyUserFactory
from users.models import CompanyUser


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_all_companies_where_user_belongs(
    api_client: APIClient, user_data: Dict[str, Any]
):
    user: CompanyUser = CompanyUserFactory.create(**user_data)
    memberships: List[Membership] = MembershipFactory.create_batch(10, user=user)
    unrelated_companies: List[Company] = CompanyFactory.create_batch(7)

    url = reverse("users:companies")

    # ensure only logged users can access
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

    # authenticate user
    api_client.login(email=user_data["email"], password=user_data["password"])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK, response.json()
    assert len(response.data) == len(memberships)

    cnpjs = [v["cnpj"] for v in response.data]
    assertion_msg = "None of unrelated companies must belong to user."
    assert all(c not in cnpjs for c in unrelated_companies), assertion_msg

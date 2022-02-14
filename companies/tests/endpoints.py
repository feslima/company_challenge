from typing import Any, Dict

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from companies.models import Company
from users.factories import CompanyUserFactory
from users.models import CompanyUser


@pytest.mark.django_db
def test_company_creation_endpoint(api_client: APIClient, company_data: Dict[str, Any]):
    # We need an already registered user on the moment the company is created
    user: CompanyUser = CompanyUserFactory.create()

    data = {"company": company_data, "user": user.email}

    url = reverse("companies:create")
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_201_CREATED, response.json()
    assert Company.objects.filter(cnpj=company_data["cnpj"]).count() == 1

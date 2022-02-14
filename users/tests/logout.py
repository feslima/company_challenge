from typing import Any, Dict

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from users.models import CompanyUser


@pytest.mark.django_db
def test_logout(
    api_client: APIClient, user_data: Dict[str, Any], registered_user: CompanyUser
):
    api_client.login(email=user_data["email"], password=user_data["password"])

    protected_url = reverse("companies:list")
    response = api_client.get(protected_url)
    assert response.status_code == status.HTTP_200_OK, response.json()

    # logging out
    url = reverse("users:logout")
    response = api_client.post(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.json()

    # protected url should fail
    response = api_client.get(protected_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

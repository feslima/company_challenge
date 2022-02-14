from typing import Any, Dict

import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from users.models import CompanyUser


@pytest.mark.django_db
def test_login(
    api_client: APIClient, user_data: Dict[str, Any], registered_user: CompanyUser
):
    # Unauthenticated request should fail
    protected_url = reverse("users:companies")
    response = api_client.get(protected_url)

    assert response.status_code == status.HTTP_403_FORBIDDEN, response.json()

    # login
    url = reverse("users:login")
    response = api_client.post(
        url, data={"email": user_data["email"], "password": user_data["password"]}
    )

    assert response.status_code == status.HTTP_200_OK, response.json()

    # Authenticated user should be able to see the protected url
    response = api_client.get(protected_url)
    assert response.status_code == status.HTTP_200_OK, response.json()

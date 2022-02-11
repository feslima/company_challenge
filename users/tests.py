import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from users.models import CompanyUser


@pytest.mark.django_db
def test_registration(api_client: APIClient, user_registration_data):
    url = reverse("users:register")

    response = api_client.post(url, data=user_registration_data)

    assert response.status_code == status.HTTP_201_CREATED, response.content.decode(
        "utf-8"
    )

    assert "password" not in response.data
    assert "password_confirm" not in response.data
    assert "email_confirm" not in response.data

    qs = CompanyUser.objects.filter(email=user_registration_data["email"])
    assert qs.count() == 1

import pytest

from users.factories import CompanyUserFactory
from users.models import CompanyUser


@pytest.fixture
def registered_user(user_data) -> CompanyUser:
    return CompanyUserFactory.create(**user_data)

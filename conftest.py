import factory
import pytest
from rest_framework.test import APIClient

from users.factories import CompanyUserFactory


@pytest.fixture
def user_data():
    """Provides user data from a factory as a dict."""
    user_data = factory.build(dict, FACTORY_CLASS=CompanyUserFactory)
    return user_data


@pytest.fixture
def user_registration_data(user_data):
    user_data["email_confirm"] = user_data["email"]
    user_data["password_confirm"] = user_data["password"]
    return user_data


@pytest.fixture
def api_client():
    """General purpose APIClient fixture. Mimics 'pytest_django' `client` fixture."""
    client = APIClient()
    return client


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    # see: https://faker.readthedocs.io/en/master/pytest-fixtures.html
    return ["pt_BR"]

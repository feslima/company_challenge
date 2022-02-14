from typing import Any, Dict

import factory
import pytest

from companies.factories import CompanyFactory


@pytest.fixture
@factory.Faker.override_default_locale("pt_BR")
def company_data() -> Dict[str, Any]:
    return factory.build(dict, FACTORY_CLASS=CompanyFactory)

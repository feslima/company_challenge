from typing import Any, Dict

import pytest
from django.core.exceptions import ValidationError
from pytest_mock import MockerFixture

import core.fields
from companies.models import Company


@pytest.mark.django_db
def test_cnpj_validation_call(mocker: MockerFixture, company_data: Dict[str, Any]):
    invalid_cnpj = "11.111.111/0001-1"
    company_data["cnpj"] = invalid_cnpj
    company = Company(**company_data)

    with pytest.raises(ValidationError) as ex:
        with mocker.patch.context_manager(core.fields, "validate_cnpj") as validator:
            company.full_clean()
        validator.assert_called()


@pytest.mark.django_db
@pytest.mark.parametrize(
    ["invalid_cnpj", "expected_error"],
    [
        ("11.111.111/0001-1", "Invalid CNPJ."),
        ("00.000.000/0001-1", "Invalid CNPJ."),
        ("00.000.000/0001-", "CNPJ must contain 14 digits."),
        ("0.000.000/0001-1", "CNPJ must contain 14 digits."),
        ("00.000.000001-1", "CNPJ must contain 14 digits."),
    ],
)
def test_cnpj_validation(invalid_cnpj: str, expected_error: str):
    with pytest.raises(ValidationError) as ex:
        core.fields.validate_cnpj(invalid_cnpj)
        assert ex.match(expected_error)

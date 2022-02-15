from datetime import datetime, timedelta
from typing import List

import factory
import pytest
from freezegun import freeze_time

from companies.factories import CompanyFactory
from companies.models import Company
from companies.services import get_companies_eligible_for_update, update_companies


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_get_companies_eligible_for_update():
    time_limit = timedelta(days=30)
    now = datetime.now()

    with freeze_time(now - (time_limit + timedelta(minutes=1))) as frozen_time:
        # "travel" to a time where the companies are considered stale
        stale: List[Company] = CompanyFactory.create_batch(10)

    recent: List[Company] = CompanyFactory.create_batch(5)

    results = get_companies_eligible_for_update(time_limit)

    cnpjs = list(results.values_list("cnpj", flat=True))
    assert results.count() == len(stale)
    assert all(c.cnpj in cnpjs for c in stale)


@pytest.mark.django_db
@factory.Faker.override_default_locale("pt_BR")
def test_company_update_service():
    """WARNING: This tests make real requests to the rate limited server, run this
    test at most 3 times per minute to avoid too many requests error."""
    cnpj = "20240272000176"
    time_limit = timedelta(days=30)
    now = datetime.now()

    with freeze_time(now - (time_limit + timedelta(minutes=1))) as frozen_time:
        company: Company = CompanyFactory.create(cnpj=cnpj)
        initial_name = company.company_name
        initial_fantasy = company.commercial_name

    update_companies()

    company.refresh_from_db()

    assert company.company_name != initial_name
    assert company.commercial_name != initial_fantasy
    assert company.last_update != company.created

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum, unique

import requests
from django.db.models import QuerySet
from django.utils import timezone

from core.validators import sanitize_cnpj

from .models import Company


@unique
class ResponseStatusEnum(Enum):
    OK = "OK"
    ERROR = "ERROR"


@dataclass
class InvalidResponse:
    message: str
    status = ResponseStatusEnum.ERROR


@dataclass
class SuccessfulResponse:
    # TODO: It does not parse the entire response, only what is needed by Company model
    status = ResponseStatusEnum.OK
    nome: str
    fantasia: str
    cnpj: str


def query_remote_api(cnpj: str):
    url = f"https://receitaws.com.br/v1/cnpj/{cnpj}"
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()

        status = ResponseStatusEnum(data["status"])
        if status == ResponseStatusEnum.ERROR:
            return InvalidResponse(message=data["message"])
        else:
            return SuccessfulResponse(
                nome=data["nome"],
                fantasia=data["fantasia"],
                cnpj=sanitize_cnpj(data["cnpj"]),
            )

    elif response.status_code == 429:
        return False, "Too many requests"
    elif response.status_code == 504:
        return False, "Timeout"
    else:
        # return the content and status for logging purposes
        return False, (response.content, response.status_code)


def get_companies_eligible_for_update(delta: timedelta) -> QuerySet[Company]:
    """Retrieve companies where the last update datetime is older than now - `delta`."""
    now = timezone.now()
    return Company.objects.filter(last_update__lte=now - delta)


def update_companies() -> None:
    companies = get_companies_eligible_for_update(timedelta(days=30))

    for company in companies:
        api_result = query_remote_api(company.cnpj)

        if isinstance(api_result, SuccessfulResponse):
            company.cnpj = api_result.cnpj
            company.company_name = api_result.nome
            company.commercial_name = api_result.fantasia
            company.last_update = timezone.now()

            company.save()
        else:
            # TODO: Log here why the update failed
            pass

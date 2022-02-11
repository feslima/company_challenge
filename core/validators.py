import re
from typing import Literal

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def sanitize_cnpj(cnpj: str) -> str:
    """Sanitizes a `cnpj` value by stripping anything that's not a numeric digit."""
    return re.sub(r"[^\d]", "", cnpj)


CNPJ_WEIGHTS = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)


def calculate_digit_cnpj(prefix: str, weight: Literal[0, 1]) -> int:
    sum_res = 0
    for idx, weight_val in enumerate(CNPJ_WEIGHTS[weight:]):
        sum_res += int(prefix[idx]) * weight_val

    rem = sum_res % 11
    digit = 0 if rem < 2 else 11 - rem

    return digit


def validate_cnpj(value: str) -> None:
    cnpj = sanitize_cnpj(value)

    if len(cnpj) != 14:
        raise ValidationError(_("CNPJ must contain 14 digits."))

    first_digit = calculate_digit_cnpj(cnpj[:-2], 1)
    if first_digit != int(cnpj[-2]):
        raise ValidationError(_("Invalid CNPJ."))

    second_digit = calculate_digit_cnpj(cnpj[:-1], 0)
    if second_digit != int(cnpj[-1]):
        raise ValidationError(_("Invalid CNPJ."))

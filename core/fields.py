from uuid import uuid4

from django.db.models import CharField, UUIDField
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from .validators import validate_cnpj


class PrimaryKeyUUIDField(UUIDField):
    """This field is equivalent to:
    >>> id = UUIDField(primary_key=True, default=uuid4, editable=False)
    """

    description = "UUIDField used as primary key in models."

    def __init__(self, *args, **kwargs):
        kwargs["primary_key"] = True
        kwargs["editable"] = False
        kwargs["default"] = uuid4
        super().__init__(*args, **kwargs)


class CNPJField(CharField):
    """Brazil's CNPJ number model field."""

    description = gettext_lazy("Brazil's CNPJ number (00.000.000/0001-00)")
    default_validators = [validate_cnpj]

    def __init__(self, *args, **kwargs):
        kwargs["verbose_name"] = "CNPJ"
        kwargs["max_length"] = 14

        kwargs["help_text"] = _(
            "Format: 14 numeric-only digits. E.g. 12.345.678/0001-12 -> 1234567800012"
        )

        super().__init__(*args, **kwargs)

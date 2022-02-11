from uuid import uuid4

from django.db.models import UUIDField


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

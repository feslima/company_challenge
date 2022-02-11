from unicodedata import normalize

import factory
from django.db.models import Model

from .models import CompanyUser, CompanyUserManager


class CompanyUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyUser

    class Params:
        full_name = factory.LazyAttribute(lambda u: f"{u.first_name} {u.surname}")

    first_name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    password = "testpass#1357"

    @classmethod
    def _create(
        cls,
        model_class: Model,
        email: str,
        first_name: str,
        surname: str,
        password: str,
        **kwargs,
    ):
        # since the model is a proxy one, we need a custom creation hook to the manager
        manager: CompanyUserManager = cls._get_manager(model_class)
        return manager.create_user(
            email=email, first_name=first_name, surname=surname, password=password
        )

    @factory.lazy_attribute
    def email(self):
        normalized_name = (
            normalize("NFKD", self.full_name).encode("ascii", "ignore").decode("utf8")
        )
        split_name = normalized_name.split()
        return "{}.{}@company.com".format(split_name[0], split_name[1]).lower()

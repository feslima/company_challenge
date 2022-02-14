import factory

from core.validators import sanitize_cnpj
from users.factories import CompanyUserFactory

from .models import Company, Membership


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    class Params:
        raw_cnpj = factory.Faker("cnpj")

    cnpj = factory.LazyAttribute(lambda o: sanitize_cnpj(o.raw_cnpj))
    corporate_name = factory.Faker("company")
    trading_name = factory.Faker("catch_phrase")


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory(CompanyUserFactory)
    company = factory.SubFactory(CompanyFactory)

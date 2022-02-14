import factory

from users.factories import CompanyUserFactory

from .models import Company, Membership


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    cnpj = factory.Faker("cnpj")
    corporate_name = factory.Faker("company")
    trading_name = factory.Faker("catch_phrase")


class MembershipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Membership

    user = factory.SubFactory(CompanyUserFactory)
    company = factory.SubFactory(CompanyFactory)

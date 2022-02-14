import factory

from .models import Company


class CompanyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Company

    cnpj = factory.Faker("cnpj")
    corporate_name = factory.Faker("company")
    trading_name = factory.Faker("catch_phrase")

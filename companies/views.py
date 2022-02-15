from django.db.models import QuerySet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import Company, Membership
from .serializers import (
    CompanyCreationSerializer,
    CompanySerializer,
    MembershipSerializer,
)


class CompanyCreationViewSet(CreateModelMixin, GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyCreationSerializer
    permission_classes = (AllowAny,)


class CompanyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)

    lookup_field = "cnpj"


class MembershipViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = MembershipSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> QuerySet[Membership]:
        return Membership.objects.filter(company__cnpj=self.kwargs["cnpj"])

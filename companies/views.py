from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from core.openapi import CNPJ_PARAMETER

from .models import Company, Membership
from .serializers import (
    CompanyCreationSerializer,
    CompanySerializer,
    MembershipSerializer,
)


class CompanyCreationViewSet(CreateModelMixin, GenericViewSet):
    """Creates a company."""

    queryset = Company.objects.all()
    serializer_class = CompanyCreationSerializer
    permission_classes = (AllowAny,)


@extend_schema_view(
    list=extend_schema(description="List all companies."),
    retrieve=extend_schema(
        description="Single company detail.", parameters=[CNPJ_PARAMETER]
    ),
)
class CompanyViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = (AllowAny,)

    lookup_field = "cnpj"


@extend_schema_view(
    list=extend_schema(
        description="List all members in this company.", parameters=[CNPJ_PARAMETER]
    ),
    create=extend_schema(
        description="Create a new member for this company.", parameters=[CNPJ_PARAMETER]
    ),
)
class MembershipViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    serializer_class = MembershipSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self) -> QuerySet[Membership]:
        return Membership.objects.filter(company__cnpj=self.kwargs["cnpj"])

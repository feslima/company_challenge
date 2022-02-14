from typing import cast

from django.db.models import QuerySet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from users.models import CompanyUser

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


class CompanyViewSet(ListModelMixin, GenericViewSet):
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Company]:
        user = cast(CompanyUser, self.request.user)  # covered by permission_classes
        return Company.objects.filter(users=user)


class MembershipViewSet(CreateModelMixin, GenericViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = (AllowAny,)

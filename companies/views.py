from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from .models import Company
from .serializers import CompanyCreationSerializer


class CompanyCreationViewSet(CreateModelMixin, GenericViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyCreationSerializer
    permission_classes = (AllowAny,)

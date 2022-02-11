from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from .serializers import CompanyUserSerializer


class CompanyUserRegisterView(CreateAPIView):
    serializer_class = CompanyUserSerializer
    permission_classes = (AllowAny,)

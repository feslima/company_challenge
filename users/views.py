from typing import cast

from django.contrib.auth import login, logout
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from companies.models import Company
from companies.serializers import CompanySerializer

from .models import CompanyUser
from .serializers import CompanyUserSerializer, LoginSerializer


class CompanyUserRegisterView(CreateAPIView):
    serializer_class = CompanyUserSerializer
    permission_classes = (AllowAny,)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    http_method_names = ["post"]

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        login(request, user)

        return Response({"success": "Login successful."}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]

    def post(self, request: Request) -> Response:
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyListView(ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Company]:
        user = cast(CompanyUser, self.request.user)  # covered by permission_classes
        return Company.objects.filter(users=user)

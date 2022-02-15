from typing import cast

from django.contrib.auth import logout
from django.db.models import QuerySet
from drf_spectacular.utils import OpenApiExample, extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from companies.models import Company
from companies.serializers import CompanySerializer

from .models import CompanyUser
from .serializers import CompanyUserSerializer, LoginSerializer


@extend_schema_view(
    post=extend_schema(
        examples=[
            OpenApiExample(
                "Signup request example",
                value={
                    "first_name": "Fulano",
                    "surname": "Cicrano Beltrano",
                    "email": "your.address@mail.com",
                    "email_confirm": "your.address@mail.com",
                    "password": "y0UrP4sSwOrD",
                    "password_confirm": "y0UrP4sSwOrD",
                },
                request_only=True,
            ),
            OpenApiExample(
                "Signup response example",
                value={
                    "email": "your.address@mail.com",
                    "first_name": "Fulano",
                    "surname": "Cicrano Beltrano",
                },
                response_only=True,
            ),
        ],
    )
)
class CompanyUserRegisterView(CreateAPIView):
    """Create a new user account."""

    serializer_class = CompanyUserSerializer
    permission_classes = (AllowAny,)


class LoginView(CreateAPIView):
    """Login an user."""

    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)
    http_method_names = ["post"]


class LogoutView(GenericAPIView):
    """Logout authenticated users on POST."""

    permission_classes = (IsAuthenticated,)
    http_method_names = ["post"]

    @extend_schema(request=None, responses={204: None})
    def post(self, request: Request) -> Response:
        logout(request)

        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyListView(ListAPIView):
    """List all the companies for current authenticated user."""

    serializer_class = CompanySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet[Company]:
        user = cast(CompanyUser, self.request.user)  # covered by permission_classes
        return Company.objects.filter(users=user)

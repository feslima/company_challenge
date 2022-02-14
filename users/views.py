from django.contrib.auth import login
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

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

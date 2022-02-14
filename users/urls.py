from django.urls import path

from .views import CompanyUserRegisterView, LoginView

urlpatterns = [
    path("register/", CompanyUserRegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
]

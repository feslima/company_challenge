from django.urls import path

from .views import CompanyUserRegisterView

urlpatterns = [path("register/", CompanyUserRegisterView.as_view(), name="register")]

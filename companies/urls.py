from django.urls import path

from .views import CompanyCreationViewSet

company_add = CompanyCreationViewSet.as_view({"post": "create"})

urlpatterns = [path("add/", company_add, name="create")]

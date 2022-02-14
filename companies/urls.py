from django.urls import path

from .views import CompanyCreationViewSet, CompanyViewSet

company_add = CompanyCreationViewSet.as_view({"post": "create"})
company_list = CompanyViewSet.as_view({"get": "list"})
urlpatterns = [
    path("add/", company_add, name="create"),
    path("list/", company_list, name="list"),
]

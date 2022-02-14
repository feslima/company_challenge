from django.urls import include, path

from .views import CompanyCreationViewSet, CompanyViewSet, MembershipViewSet

company_add = CompanyCreationViewSet.as_view({"post": "create"})
company_list = CompanyViewSet.as_view({"get": "list"})
member_add = MembershipViewSet.as_view({"post": "create"})

members_patterns = [
    path("new/", member_add, name="create"),
]

urlpatterns = [
    path("add/", company_add, name="create"),
    path("list/", company_list, name="list"),
    path("members/", include((members_patterns, "members"), namespace="members")),
]

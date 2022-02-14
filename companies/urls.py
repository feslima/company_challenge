from django.urls import include, path, register_converter

from .views import CompanyCreationViewSet, CompanyViewSet, MembershipViewSet

member_add = MembershipViewSet.as_view({"post": "create"})
member_list = MembershipViewSet.as_view({"get": "list"})
members_patterns = [
    path("", member_list, name="list"),
    path("add/", member_add, name="create"),
]


class CNPJConverter:
    """Converts to/from urls following the CNPJ format of 14 numeric digits."""

    regex = r"\d{14}"

    def to_python(self, value: str) -> str:
        return value

    def to_url(self, value: str) -> str:
        return value


register_converter(CNPJConverter, "cnpj")

company_add = CompanyCreationViewSet.as_view({"post": "create"})
company_detail = CompanyViewSet.as_view({"get": "retrieve"})
urlpatterns = [
    path("<cnpj:cnpj>/", company_detail, name="detail"),
    path("add/", company_add, name="create"),
    path(
        "<cnpj:cnpj>/members/",
        include((members_patterns, "members"), namespace="members"),
    ),
]

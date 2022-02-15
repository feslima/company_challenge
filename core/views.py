from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.permissions import AllowAny


class SwaggerSchemaView(SpectacularSwaggerView):
    permission_classes = [AllowAny]
    url_name = "schema"

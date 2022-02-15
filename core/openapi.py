from drf_spectacular.utils import OpenApiExample, OpenApiParameter

CNPJ_PARAMETER = OpenApiParameter(
    name="cnpj",
    description="Brazil's 14 numeric digits CNPJ.",
    location=OpenApiParameter.PATH,
    examples=[
        OpenApiExample(
            "Format",
            description="12.345.678/0001-12 must be typed as 1234567800012",
            value="12345678000112",
        )
    ],
)

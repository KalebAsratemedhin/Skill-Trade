from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView



urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/auth/", include("users.urls")),
    path("api/bookings/", include("bookings.urls")),

    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Swagger UI
    # path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    
    # # Redoc UI
    # path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    
    # # Raw JSON/YAML Schema
    # path("swagger.json", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    # path("swagger.yaml", schema_view.without_ui(cache_timeout=0), name="schema-yaml"),
]

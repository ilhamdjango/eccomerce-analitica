from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path('admin/', admin.site.urls),

    # App endpoints
    path('api/v1/', include('analitic.urls')),
    path('api/v2/', include('analitic.urls')),

    # OpenAPI JSON
    path('openapi.json', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # Redoc UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Boş path '/' → Swagger UI-ə yönləndirilir
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='home'),
]


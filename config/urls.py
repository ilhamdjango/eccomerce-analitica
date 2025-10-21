from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.renderers import JSONRenderer


class CustomSpectacularAPIView(SpectacularAPIView):
    renderer_classes = [JSONRenderer]


urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/', include('analitic.urls')),
    path('api/v2/', include('analitic.urls')),

    # OpenAPI JSON
    path('openapi.json', CustomSpectacularAPIView.as_view(), name='schema-json'),

    # Swagger UI
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),

    # Redoc UI
    path('redoc/', SpectacularRedocView.as_view(url_name='schema-json'), name='redoc-ui'),

    # Default path redirecting to Swagger UI
    path('', SpectacularSwaggerView.as_view(url_name='schema-json'), name='swagger-ui'),
]

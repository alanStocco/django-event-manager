from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path

from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title="Event Manager API",
        default_version='v1',
        description="API for managing events",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@eventmanager.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

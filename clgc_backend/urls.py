from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema = get_schema_view(
    openapi.Info(
        title="Swagger docs for church API",
        name="Church Backend API",
        default_version="v0.0.1",
        description="API for City of Light Global Church Application"
    ),
    permission_classes=(AllowAny,),
    public=True,
    # url="https://clgcchurch-backend-production.up.railway.app",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/members/', include('members.urls')),
    path("api/auth/",include("auths.urls")),
    path("api/",include("user.urls")),  
    path("swagger/docs",schema.with_ui("swagger",cache_timeout=0),name="swagger-api"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for clgc_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
    url="https://clgcchurch-backend-production.up.railway.app",
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/', include('members.urls')),
    path("api/auth/",include("auths.urls")),
    path("api/",include("user.urls")),  
    path("swagger/docs",schema.with_ui("swagger",cache_timeout=0),name="swagger-api"),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

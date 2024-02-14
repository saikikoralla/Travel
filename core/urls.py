
from django.contrib import admin
from django.urls import path,include

#from drf_yasg.views import get_schema_view
#from drf_yasg import openapi
from rest_framework import permissions


"""schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="My API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="Awesome License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)"""
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',include(('users.urls','users'),namespace='users')),
    path('api/packages/',include(('packages.urls','packages'),namespace='packages')),
    #path('api/triprecords/',include(('TripRecords.urls','TripRecords'),namespace='triprecords')),
    path('auth/', include('rest_framework.urls'), name='rest_framework'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
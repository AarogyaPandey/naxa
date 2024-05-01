
from django.contrib import admin
from django.urls import path, include
from todo import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/task/', include('todo.urls')),
    path('api/user/', include('user.urls')),
    path('api/geo/', include('geospatial.urls')),
    path('api/map/', include('map.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

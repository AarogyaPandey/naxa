
from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/task/', include('todo.urls')),
    path('api/user/', include('user.urls')),
    path('api/geo/', include('geospatial.urls')),
]

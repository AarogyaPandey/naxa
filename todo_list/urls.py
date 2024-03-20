
from django.contrib import admin
from django.urls import path, include
from todo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('todo/', views.TodoViewSet.as_view({'get':'list'})),
]

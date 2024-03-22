from django.urls import path, include
from .views import TodoViewSet
from .models import Task
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'task',TodoViewSet)

urlpatterns=[
     path('', include(router.urls)),
     path('todo/', TodoViewSet.as_view({'get': 'list'}), name='todo-list'),  # Use TodoViewSet for listing
     path('todo/<int:pk>/', TodoViewSet.as_view({'get': 'retrieve'}), name='todo-detail')  # Use TodoViewSet for detail

]
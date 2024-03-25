from django.urls import path, include
from .views import TodoViewSet, TodoDetails
from .models import Task
from rest_framework.routers import DefaultRouter
from . import views

router=DefaultRouter()
router.register(r'task',TodoViewSet)

urlpatterns=[
     path('', include(router.urls)),
     path('todo/', TodoViewSet.as_view({'get': 'list'}), name='todo-list'),  # Use TodoViewSet for listing
     path('todo/<int:pk>/', TodoViewSet.as_view({'get': 'retrieve'}), name='todo-detail'),  # Use TodoViewSet for detail
     path('get_val/', views.todo_details, name='get_val'),
     path('post_val/', views.todo_post, name='post_val'),
     path('todo-details/', TodoDetails.as_view(), name='todo-details'),
]
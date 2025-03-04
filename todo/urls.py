from django.urls import path, include
from .views import TodoViewSet, TodoDetails
from .models import Task
from rest_framework.routers import DefaultRouter
from .views import *

router=DefaultRouter()
router.register(r'task',TodoViewSet)

urlpatterns=[
     path('', include(router.urls)),
     path('todo/', TodoViewSet.as_view({'get': 'list'}), name='todo-list'), 
     # path('todo/<int:pk>/', TodoViewSet.as_view({'get': 'retrieve'}), name='todo-detail'), 
     path('get_val/', todo_details, name='get_val'),
     path('post_val/', todo_post, name='post_val'),
     path('todo-details/', TodoDetails.as_view(), name='todo-details'),
     path('todos/<str:pk>/post/', TodoPost.as_view(), name='todo-post'),
     path('todos/<str:pk>/del/', TodoDelete.as_view(), name='todo-del'),
     path('todos/<str:pk>/patch/', TodoPatch.as_view(), name='todo-patch'),
     path('todos/<str:pk>/put/', TodoPut.as_view(), name='todo-put'),
     path('get_list/', task_list, name='get_list'),
]
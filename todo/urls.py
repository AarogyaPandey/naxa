from django.urls import path, include
# from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginVie, TodoViewSet
from .views import TodoViewSet
from .models import Task
from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'task',TodoViewSet)

urlpatterns=[
     path('', include(router.urls))
    # path('todoos/', )
    # path('login/', CustomLoginView.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    # path('', TaskList.as_view(), name='tasks'),
    # path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    # path('task-create/', TaskCreate.as_view(), name='task-create'),
    # path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    # path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
]
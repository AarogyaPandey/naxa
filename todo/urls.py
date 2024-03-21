from django.urls import path, include
from .views import TodoViewSet
from .models import Task
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'task',TodoViewSet)

urlpatterns=[
     path('', include(router.urls))

]
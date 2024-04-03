from user.views import SignUp, postapi
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router=DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', postapi, name='login'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from map.views import LayerViewSet, GetApi
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from map.views import LayerViewSet, GetApi

router=DefaultRouter()
router.register(r'layers',LayerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('getapi/', GetApi.as_view(), name='getapi')
]

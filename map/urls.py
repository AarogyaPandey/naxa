from django.urls import path, include
from rest_framework.routers import DefaultRouter
from map.views import LayerViewSet, GetApi, GetLayer
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from map.views import LayerViewSet, GetApi, GetLayer

router=DefaultRouter()
router.register(r'layers',LayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('getapi/', GetApi.as_view(), name='getapi'),
    path('getlayer/', GetLayer.as_view(), name='getlayer')
]

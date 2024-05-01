from django.urls import path, include
from rest_framework.routers import DefaultRouter
from map.views import LayerViewSet 

router=DefaultRouter()
router.register(r'layers',LayerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

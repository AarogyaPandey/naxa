from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from geospatial.views import GeoSpatial, Geom


router=DefaultRouter()
router.register(r'geos',GeoSpatial)
urlpatterns = [
    path('', include(router.urls)),
    path('postgeom/', Geom.as_view(), name='postgeom'),
    
]

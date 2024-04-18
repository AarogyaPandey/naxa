from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from geospatial.views import GeoSpatial, Geom, GetApi, JsonResponse, JsonResponseShp, BankPost, BankGet, download, palikafilter

router=DefaultRouter()
router.register(r'geos',GeoSpatial)

urlpatterns = [
    
    path('', include(router.urls)),
    path('postgeom/', Geom.as_view(), name='postgeom'),
    path('getapi/', GetApi.as_view(), name='getapi'),
    path('jsonresponse/', JsonResponse.as_view(), name='jsonresponse'),
    path('shpres/', JsonResponseShp.as_view(), name='shpresp'),
    path('bankpost/', BankPost.as_view(), name='bankpost'),
    path('bankget/', BankGet.as_view(), name='bankget'),
    path('download/', download, name='download'),
    path('palikafilter/', palikafilter, name='palikafilter'),

]
from django.urls import path, include
from rest_framework.routers import  DefaultRouter
from geospatial.views import GeoSpatial, Geom, GetApi, JsonResponse, JsonResponseShp, BankPost, BankGet
from django.conf import settings
from django.conf.urls.static import static


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
    # path('getapijson/', GetApiJson.as_view(), name='getapijson'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


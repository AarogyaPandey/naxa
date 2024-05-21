from django.urls import path, include
from rest_framework.routers import DefaultRouter
from map.views import LayerViewSet, GetApi, GetLayer,upload_csv, download_csv
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from map.views import LayerViewSet, GetApi, GetLayer

router=DefaultRouter()
router.register(r'layers',LayerViewSet)
# router.register(r'category',CategoryList)

urlpatterns = [
    path('', include(router.urls)),
    path('getapi/', GetApi.as_view(), name='getapi'),
    path('getlayer/', GetLayer.as_view(), name='getlayer'),
    path('csvupload/', upload_csv, name='csvupload'),
    path('csvdownload/', download_csv, name='csvdownload')
]

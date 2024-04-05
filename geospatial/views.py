from django.shortcuts import render
from rest_framework import viewsets
from geospatial.models import GeoSpatialData
from geospatial.serializers import  GeoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework.decorators import permission_classes, authentication_classes

class GeoSpatial(viewsets.ModelViewSet):
    queryset= GeoSpatialData.objects.all()
    serializer_class=GeoSerializer
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]
    
    def  create(self, request, *args, **kwargs):
        file_type=request.query_params.get('file_type', None)
        if file_type=="True":
            self.queryset=GeoSpatialData.objects.filter(file_type=True)
            
        else:
            self.queryset=GeoSpatialData.objects.all()
        return super().create(request, *args, **kwargs)    
    

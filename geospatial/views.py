from django.shortcuts import render
from rest_framework import viewsets
from geospatial.models import GeoSpatialData, PalikaGeometry, PalikaUpload
from geospatial.serializers import  GeoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import  APIView
from rest_framework.response import Response
from geopandas import geopandas  as gpd
from django.contrib.gis.geos import GEOSGeometry
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
    

class Geom(APIView):
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        try:
            shp = request.data.get('shp')
            if shp:
                gdf = gpd.read_file(shp)
                for index, row in gdf.iterrows():
                    geom = GEOSGeometry(str(row['geometry']))
                    attr_data= row.drop(['geometry']).to_dict()
                    state= attr_data.pop("STATE")
                    district=str(row['DISTRICT'])
                    area=geom.area*111.32*111.32
                    bbox=geom.extent
                    bbox_width=bbox[2]-bbox[0]
                    bbox_height=bbox[3]-bbox[1]
                    bbox_area=bbox_width*bbox_height*111.32*111.32
                    PalikaGeometry.objects.create(geom=geom,district=district, state=state,area=area,bbox_area=bbox_area, bbox=bbox, extra_json=attr_data, user=request.user)
                    
                return Response('Shapefile uploaded successfully')
            else:
                return Response('No shapefile provided')
        except Exception as e:
            return Response(f'Error uploading shapefile: {str(e)}')
        

                      


from django.shortcuts import render
from rest_framework import viewsets
from geospatial.models import GeoSpatialData, PalikaGeometry, PalikaUpload, JsonGeometry
from geospatial.serializers import  GeoSerializer, PalikaGeometrySerializer,  UploadSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import  APIView
from rest_framework.response import Response
from geopandas import geopandas  as gpd
from django.contrib.gis.geos import GEOSGeometry
import json
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
            file = request.data.get('file')
            file_type=request.data.get("file_type")
            
            if not file_type:
                return Response("File type is required")
            serializer=UploadSerializer(data=request.data)
            
            if serializer.is_valid():
                obj=serializer.save()
                
            if file_type=="shapefile":
                gdf = gpd.read_file(file)
                
                for index, row in gdf.iterrows():
                    geom = GEOSGeometry(str(row['geometry']))
                    attr_data= row.drop(['geometry']).to_dict()
                    ward_number= attr_data.pop("NEW_WARD_N")
                    description=attr_data.pop("CENTER")
                    district=attr_data.pop("DISTRICT")
                    palika_name=attr_data.pop("dname")
                    area_gdf = gpd.GeoDataFrame(geometry=[row["geometry"]], crs=gdf.crs)
                    area_gdf.to_crs(epsg=3857, inplace=True)
                    area = area_gdf.area.iloc[0] / 1000000
                    bbox=geom.extent
                    bbox_width=bbox[2]-bbox[0]  
                    bbox_height=bbox[3]-bbox[1]
                    bbox_area=bbox_width*bbox_height*111.32*111.32
                    PalikaGeometry.objects.create(geom=geom,palikaupload=obj, palika_name=palika_name, description=description, area=area,ward_number=ward_number,district=district, bbox_area=bbox_area, bbox=bbox, extra_json=attr_data, user=request.user)
                    
                return Response('Shapefile uploaded successfully')
            elif file_type=="geojson":
                gdf=gpd.read_file(file)
                for index, row in gdf.iterrows():
                    geom = GEOSGeometry(str(row['geometry']))
                    attr_data=row.drop(["geometry"]).to_dict()
                    ward_number= attr_data.pop("NEW_WARD_N")
                    description=attr_data.pop("CENTER")
                    district=attr_data.pop("DISTRICT")
                    palika_name=attr_data.pop("dname")
                    area_gdf = gpd.GeoDataFrame(geometry=[row["geometry"]], crs=gdf.crs)
                    area_gdf.to_crs(epsg=3857, inplace=True)
                    area = area_gdf.area.iloc[0] / 1000000
                    bbox=geom.extent
                    bbox_width=bbox[2]-bbox[0]  
                    bbox_height=bbox[3]-bbox[1]
                    bbox_area=bbox_width*bbox_height*111.32*111.32
                    JsonGeometry.objects.create(geom=geom,palikaupload=obj, palika_name=palika_name, description=description, area=area,ward_number=ward_number,district=district, bbox_area=bbox_area, bbox=bbox, extra_json=attr_data, user=request.user)
                return Response('Successful Upload of GeoJson!')
                                        
            else:
                return Response('No shapefile provided')
        except Exception as e:
            return Response(f'Error uploading shapefile: {str(e)}')
        

                      


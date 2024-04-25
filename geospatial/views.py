from django.shortcuts import render
from rest_framework import viewsets
from geospatial.models import GeoSpatialData, PalikaGeometry, PalikaUpload, JsonGeometry, BankGeometry, WeatherForecast
from geospatial.serializers import  GeoSerializer, PalikaGeometrySerializer,  UploadSerializer, JsonGeometrySerializer, BankGeometrySerializer, WeatherForecastSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import  APIView
from rest_framework.response import Response
from geopandas import geopandas  as gpd
from django.contrib.gis.geos import GEOSGeometry
import json
from django.core.serializers import serialize
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from geospatial.geojsonapi import processapi
import openmeteo_requests
# import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta

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
            file = request.data.get('data_file')
            file_type=request.data.get("file_type")
            
            if not file_type:
                return Response("File type is required") 
            
            serializer=UploadSerializer(data=request.data)
            if serializer.is_valid():
                obj=serializer.save()
                print("this is the object", obj.id)
                
            if file_type=="shapefile":
                gdf = gpd.read_file(obj.data_file.path)
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
                    PalikaGeometry.objects.create(geom=geom, palikaupload=obj, 
                                                  palika_name=palika_name, description=description, 
                                                  area=area,ward_number=ward_number,
                                                  district=district, bbox_area=bbox_area,
                                                  bbox=bbox, extra_json=attr_data, user=request.user)
                return Response('Shapefile uploaded successfully')
            elif file_type=="geojson": 
                print("is geo json") 
                processapi(obj.data_file.path,request.user.id,obj.id)
                return Response("The data is being uploaded...")                          
        except Exception as e:
            return Response(f'Error uploading shapefile: {str(e)}')
        
class GetApi(APIView):
    def get(self, request):
        task=PalikaGeometry.objects.all()
        serializer=PalikaGeometrySerializer(task, many=True)
        obj=serializer.data
        return Response(obj, content_type='application/json', status=200)
    
class JsonResponse(APIView):
    def get(self, request):
        query=JsonGeometry.objects.all()
        data=serialize('geojson',query, geometry_field="geom")
        data=json.loads(data)
        return Response(data, content_type='application/json')
    
class JsonResponseShp(APIView):
    def get(self, request):
        query=PalikaGeometry.objects.all()
        data=serialize('geojson',query, geometry_field="geom")
        data=json.loads(data)
        return Response(data, content_type='application/json')
    
class BankGet(APIView):
    def get(self, request):
        query=BankGeometry.objects.all()
        data=serialize('geojson', query, geometry_field="geom")
        data=json.loads(data)
        return Response(data, content_type='application/json')
    
class BankPost(APIView):
    def post(self, request):
        try:
            file=request.data.get('file')
            file_type=request.data.get('file_type')
            
            if not file_type:
                return Response("File type is required")
            serializer=UploadSerializer(data=request.data)
            
            if serializer.is_valid():
                obj=serializer.save()
                
            if file_type=='geojson':
                gdf=gpd.read_file(file)
                for index, row in gdf.iterrows():
                    geom=GEOSGeometry(str(row['geometry']))
                    attr_data=row.drop(['geometry']).to_dict()
                    amenity=attr_data.pop("amenity")
                    name_en=attr_data.pop("name:en")
                    name_ne=attr_data.pop("name:ne")
                    timestamp=attr_data.pop("@timestamp")
                    BankGeometry.objects.create(geom=geom, palikaupload=obj,amenity=amenity, 
                                                name_en=name_en, name_ne=name_ne, timestamp=timestamp, extra_json=attr_data) 
                    
                return Response('Successful GeoJson Upload!')
            else:
                return Response('No GeoJson file provided')
        except Exception as e:
            return Response(f"Error uploading file: {str(e)}")
        
@api_view(["GET"])
def download(request):
    query = PalikaGeometry.objects.all()
    geojson_data = serialize('geojson', query, geometry_field='geom')
    response = HttpResponse(geojson_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="data.geojson"'
    return response

@api_view(['GET'])
def palikafilter(request):
    ward_no=request.query_params.get('ward' ,None)
    if ward_no:
        query=PalikaGeometry.objects.filter(ward_number=ward_no)
        serializer=PalikaGeometrySerializer(query, many=True)
        return Response(serializer.data)
    else:
        return Response("ward number is required", status=400)

# =====================================================================================     
# @api_view(['GET'])
# def get_current_weather(request):
#     """
#     Get the current weather data for a specific location.
#     """

# class WeatherApi(APIView):
#     def post(self, request):
#         retry_session = retry(retries = 5, backoff_factor = 0.2)
#         openmeteo = openmeteo_requests.Client(session = retry_session)
        
#         url = "https://api.open-meteo.com/v1/forecast"
#         params = {
#             "latitude": 27.15,
#             "longitude": 85.9,
#             "hourly": ["temperature_2m", "precipitation_probability", "precipitation", "rain"],
#             "timezone":"auto",
#         }
#         responses = openmeteo.weather_api(url, params=params)

#         response = responses[0]
#         print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
#         print(f"Elevation {response.Elevation()} m asl")
#         print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
#         print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

#         hourly = response.Hourly()
#         hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
#         hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
#         hourly_precipitation = hourly.Variables(2).ValuesAsNumpy()
#         hourly_rain = hourly.Variables(3).ValuesAsNumpy()
#         hourly_data = {"date": pd.date_range(
#             start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
#             end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
#             freq = pd.Timedelta(seconds = hourly.Interval()),
#             inclusive = "left"
#         )}
#         hourly_data["temperature_2m"] = hourly_temperature_2m[0]
#         hourly_data["precipitation_probability"] = hourly_precipitation_probability[0]
#         hourly_data["precipitation"] = hourly_precipitation[0]
#         hourly_data["rain"] = hourly_rain[0]
#         date_value = pd.to_datetime(hourly.Time(), unit="s")
        
#         obj = WeatherForecast.objects.create(temperature_2m=float(hourly_data["temperature_2m"]), rain=float(hourly_data["rain"]), 
#                                              precipitation_probability=float(hourly_data["precipitation_probability"]), 
#                                              precipitation=float(hourly_data["precipitation"]),date= date_value)
#         print(obj)
#         return Response(hourly_data)
#  ======================================================================================

class WeatherApi(APIView):
    def post(self, request):
        retry_session = retry(retries = 5, backoff_factor = 0.2)
        openmeteo = openmeteo_requests.Client(session = retry_session)

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 27.15,
            "longitude": 85.9,
            "current": ["relative_humidity_2m", "apparent_temperature", "precipitation", "rain"],
            "timezone": "auto",
            "forecast_days": 1
        }
        responses = openmeteo.weather_api(url, params=params)

        response = responses[0]
        print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation {response.Elevation()} m asl")
        print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
        print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

        current = response.Current()
        current_relative_humidity_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_precipitation = current.Variables(2).Value()
        current_rain = current.Variables(3).Value()
        print(current_apparent_temperature)
        
        hourly_data = {"date": pd.date_range(
            start = pd.to_datetime(current.Time(), unit = "s", utc = True),
            end = pd.to_datetime(current.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = current.Interval()),
            inclusive = "left"
        )}
        hourly_data["temperature_2m"] = current_apparent_temperature
        hourly_data["humidity"] = current_relative_humidity_2m
        hourly_data["precipitation"] = current_precipitation
        hourly_data["rain"] = current_rain
        # date_value = pd.to_datetime(current.Time(), unit="s")
        

        date_value = pd.to_datetime(current.Time(), unit="s") + timedelta(hours=5, minutes=52)

        
        obj = WeatherForecast.objects.create(temperature_2m=float(hourly_data["temperature_2m"]), rain=float(hourly_data["rain"]), 
                                             humidity=float(hourly_data["humidity"]), 
                                             precipitation=float(hourly_data["precipitation"]),date= date_value)
        print(obj)
        print(f"Current time {current.Time()}")
        print(f"Current relative_humidity_2m {current_relative_humidity_2m}")
        print(f"Current apparent_temperature {current_apparent_temperature}")
        print(f"Current precipitation {current_precipitation}")
        print(f"Current rain {current_rain}")
        return Response(WeatherForecast.objects.filter(id=obj.id).values())
    





    




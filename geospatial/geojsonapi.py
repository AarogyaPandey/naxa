from celery import shared_task
from rest_framework.response import  Response
import json
from  .models import JsonGeometry
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry
import geopandas as gpd
from geospatial.models import PalikaUpload, WeatherForecast
import openmeteo_requests
# import requests_cache
import pandas as pd
from retry_requests import retry
from datetime import timedelta


@shared_task
def processapi(data_file,user_id,file_id):
    file_obj = PalikaUpload.objects.get(id = file_id)
    print(f"file path: {data_file}")
    gdf = gpd.read_file(data_file)
    print("check check")
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
        JsonGeometry.objects.create(geom=geom, palikaupload = file_obj,
                                    palika_name=palika_name, description=description, 
                                    area=area,ward_number=ward_number,district=district, 
                                    bbox_area=bbox_area, bbox=bbox, extra_json=attr_data, user_id=user_id)
                                            
    return Response('geojson file uploaded successfully')
@shared_task
def weatherpostapi():
    
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
    # return Response(WeatherForecast.objects.filter(id=obj.id).values())
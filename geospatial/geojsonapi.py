from celery import shared_task
from rest_framework.response import  Response
import json
from  .models import JsonGeometry
from django.core.serializers import serialize
from django.contrib.gis.geos import GEOSGeometry
import geopandas as gpd
from geospatial.models import PalikaUpload

@shared_task
def processapi(data_file,user_id): 
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
        JsonGeometry.objects.create(geom=geom, 
                                    palika_name=palika_name, description=description, 
                                    area=area,ward_number=ward_number,district=district, 
                                    bbox_area=bbox_area, bbox=bbox, extra_json=attr_data, user_id=user_id)
                                            
    return Response('geojson file uploaded successfully')

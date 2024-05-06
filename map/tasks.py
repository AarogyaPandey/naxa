from django.test import TestCase
from map.models import Layer
import os
import geopandas as gpd
from django.contrib.auth.models import User
from django.contrib.gis.geos import GEOSGeometry
from map.models import FeatureCollection, Category
# Create your tests here.
def process_layer(layer_id, user_id, category):
    layer=Layer.objects.get(id=layer_id)
    file=str(layer.file_upload.path)
    split_tup=os.path.splitext(file)
    file_extension=split_tup[1]
    try:
        if file_extension.lower()==".zip":
            shapefile=file
           
            try:
                gdf=gpd.read_file(shapefile)
                geometry_type=gdf["geometry"].iloc[0].geom_type
                total_bounds=gdf.total_bounds
                bound_dict={"total_bounds": total_bounds.tolist()}
                user_instance=User.objects.get(id=user_id)
                for index, row in gdf.iterrows():
                    dropped_geometry=row.drop(["geometry"])
                    geom=GEOSGeometry(str(row["geometry"]))
                    attr_data=dropped_geometry.to_dict()
                    FeatureCollection.objects.create(
                        layer_id=layer_id,
                        attr_data=attr_data,
                        geom=geom,
                        created_by=user_instance
                        
                    )

                    layer.category_id=category
                    layer.geom_type=geometry_type
                    layer.bbox=bound_dict
                    layer.created_by=user_instance
                    layer.save()
                    

            except Exception as e:
                return str(e)
    except Exception as e:
        return str(e)
    
                

            
                
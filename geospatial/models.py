from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismd
# from modeltranslation.translator import TranslationOptions, register

# @register
class  GeoSpatialData(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    username = models.CharField(max_length=100, blank=True, null=True)
    palika_name=models.CharField(max_length=100, blank=True, null=True)
    geom= gismd.GeometryField(srid=4326, null=True, blank=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    file_type=models.CharField(max_length=100, blank=True, null=True) 
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    data_file=models.FileField(upload_to= 'geospatialdata/', blank=True, null=True)
    
    def __str__(self):
        return self.username
    
class PalikaUpload(models.Model):
    data_file=models.FileField(upload_to= 'geospatialdata/' ,blank=True, null=True)
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    
    
class PalikaGeometry(models.Model):
    file_type_choices=[
    ('shapefile', 'Shapefile'),
    ('geojson', "GeoJSON")
]
    user=models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    palikaupload=models.ForeignKey(PalikaUpload, on_delete=models.CASCADE, blank=True, null=True)
    palika_name=models.CharField(max_length=100, blank=True, null=True)
    file_type=models.CharField(max_length=100, choices=file_type_choices, blank=True, null=True, default=('shapefile'))
    geom= gismd.GeometryField(srid=4326, null=True, blank=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    district=models.CharField(max_length=100, blank =True, null=True)
    state=models.CharField(max_length=100, blank=True, null=True)
    area=models.FloatField(null=True, blank=True)
    bbox_area=models.FloatField(null=True, blank=True)
    bbox=models.CharField(max_length=200, blank=True, null=True)
    extra_json=models.JSONField(null=True, blank=True) # for storing any other json field data which is not covered 
    

    
    
# class GeoSpatialDataTranslate(TranslationOptions):
#     fields=('description', 'name')


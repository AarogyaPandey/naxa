from django.db import models
from django.contrib.auth.models import User
# from modeltranslation.translator import TranslationOptions, register

# @register
class  GeoSpatialData(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, blank=True, null=True)
    description=models.TextField(max_length=1000, blank=True, null=True)
    file_type=models.CharField(max_length=100, blank=True, null=True) #ex: shapefile or csv or geojson
    upload_date=models.DateTimeField(auto_now_add=True, null=True,  blank=True)
    data_file=models.FileField(upload_to= 'geospatialdata/')
    
    def __str__(self):
        return self.name
    
  
# class GeoSpatialDataTranslate(TranslationOptions):
#     fields=('description', 'name')


from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismd

class Category(models.Model):
    name_en=models.CharField(max_length=200, blank=True, null=True)
    name_ne=models.CharField(max_length=200, blank=True, null=True)
    description_en=models.TextField(max_length=500,blank=True, null=True)
    description_ne=models.TextField(max_length=500,blank=True, null=True)
    bbox=models.JSONField(default=dict, null=True, blank=True)
    geom_type=models.CharField(max_length=100, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
def __str__(self):
    return str(self.id)


class Layer(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name= "layers",null=True, blank=True)
    file_upload=models.FileField(upload_to='map', blank=True, null=True)
    layer_name_en=models.CharField(max_length=200, blank=True, null=True)
    layer_name_ne=models.CharField(max_length=200, blank=True, null=True)
    description_en=models.TextField(max_length=500,blank=True, null=True)
    description_ne=models.TextField(max_length=500,blank=True, null=True)
    bbox=models.JSONField(default=dict, null=True, blank=True)
    geom_type=models.CharField(max_length=100, null=True, blank=True)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user_layers")

class FeatureCollection(models.Model):
    layer=models.ForeignKey(Layer, on_delete=models.CASCADE,related_name='feature',blank=True, null=True)
    geom=gismd.GeometryField(srid=4326, null=True, blank=True)
    attr_data=models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_layer_feature')
    
class CsvUpload(models.Model):
    file_upload=models.FileField(upload_to='map', blank=True, null=True)
    created_by=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_csv')
    created_at=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status=models.CharField(max_length=100, blank=True, null=True)
    error=models.TextField(max_length=500, blank=True, null=True)
    layer=models.ForeignKey(Layer, on_delete=models.CASCADE, related_name='csv_layer', blank=True, null=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE, related_name='csv_category', blank=True, null=True)
    
    def __str__(self):
        return self.file_upload.name
    
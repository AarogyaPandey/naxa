from rest_framework import serializers
from geospatial.models import GeoSpatialData, PalikaGeometry, PalikaUpload, JsonGeometry, BankGeometry

class  GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSpatialData
        fields = '__all__'
        
class  UploadSerializer(serializers.ModelSerializer):
    class Meta:
        model= PalikaUpload
        fields='__all__'
    
class PalikaGeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model=  PalikaGeometry
        fields='__all__'
        
class JsonGeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model= JsonGeometry
        fields='__all__'
        
class JsonGeometrySerializer(serializers.ModelSerializer):
    class Meta:
        model= JsonGeometry
        fields='__all__'  
from rest_framework import serializers
from map.models import Category, FeatureCollection, Layer, CsvUpload

class  CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class  FeatureColletionSerializer(serializers.ModelSerializer):
    class Meta:
        model= FeatureCollection
        fields='__all__'
    
class LayerSerializer(serializers.ModelSerializer):
    class Meta:
        model=  Layer
        fields='__all__'
        
class CsvSerializer(serializers.ModelSerializer):
    class Meta:
        model=  CsvUpload
        fields='__all__'
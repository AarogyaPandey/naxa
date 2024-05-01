from rest_framework import serializers
from map.models import Category, FeatureCollection, Layer

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
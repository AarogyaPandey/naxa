from rest_framework import serializers
from geospatial.models import GeoSpatialData

class  GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSpatialData
        fields = ('id', 'username', 'palika_name', 'user', 'geom',  'file_type', 'description', 'data_file', 'upload_date')
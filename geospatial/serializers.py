from rest_framework import serializers
from geospatial.models import GeoSpatialData, PalikaGeometry, PalikaUpload

class  GeoSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoSpatialData
        # fields = ('id', 'username', 'palika_name', 'geom',  'file_type', 'description', 'data_file', 'upload_date')
        fields = '__all__'
        # exclude_fields =
        model=PalikaGeometry
        fields=('palikaupload', 'palika_name', 'geom', 'description', 'upload_date')
        model=PalikaUpload
        fields=('data_file', 'upload_date')
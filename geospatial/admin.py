from django.contrib import admin
from geospatial.models import GeoSpatialData, PalikaUpload, PalikaGeometry, JsonGeometry, BankGeometry, WeatherForecast

class GeoSpatialDataAdmin(admin.ModelAdmin):
    list_display=['user', 'username','geom', 'palika_name', 'description', 'file_type', 'upload_date', 'data_file']
    
class PalikaUploadAdmin(admin.ModelAdmin):
    list_display=['data_file', 'upload_date']
    
class PalikaGeometryAdmin(admin.ModelAdmin):
    list_display=['palikaupload', 'palika_name', 'description', 'upload_date']
    
class JsonGeometryAdmin(admin.ModelAdmin):
    list_display=['palikaupload', 'palika_name', 'description', 'upload_date']
    
class BankGeometryAdmin(admin.ModelAdmin):
    list_display=['name_ne', 'name_en', 'amenity']
    
class WeatherForecastAdmin(admin.ModelAdmin):
    list_display=['precipitation', 'temperature_2m', 'rain','humidity', 'date']

admin.site.register(GeoSpatialData, GeoSpatialDataAdmin)
admin.site.register(PalikaUpload, PalikaUploadAdmin)
admin.site.register(PalikaGeometry, PalikaGeometryAdmin)
admin.site.register(JsonGeometry, JsonGeometryAdmin)
admin.site.register(BankGeometry, BankGeometryAdmin)
admin.site.register(WeatherForecast, WeatherForecastAdmin)
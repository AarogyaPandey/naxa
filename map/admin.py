from django.contrib import admin
from map.models import Category, Layer, FeatureCollection, CsvUpload
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name_en', 'geom_type', 'created_at']

class LayerAdmin(admin.ModelAdmin):
    list_display=['id','file_upload', 'geom_type', 'category']

class FeatureCollectionAdmin(admin.ModelAdmin):
    list_display=['id','layer', 'created_at', 'created_by']

class CsvUploadAdmin(admin.ModelAdmin):
    list_display=['id','file_upload', 'status', 'created_at', 'created_by']
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(FeatureCollection, FeatureCollectionAdmin)
admin.site.register(CsvUpload, CsvUploadAdmin)

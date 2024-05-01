from django.contrib import admin
from map.models import Category, Layer, FeatureCollection
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name_en', 'geom_type', 'created_at']
    # list_display=[field.name for field in Category._meta.get_fields() if not field.many_to_many]

class LayerAdmin(admin.ModelAdmin):
    list_display=['id','file_upload', 'geom_type', 'category']
    # list_display=[field.name for field in Layer._meta.get_fields() if not field.many_to_many]

class FeatureCollectionAdmin(admin.ModelAdmin):
    list_display=['id','layer', 'created_at', 'created_by']
    # list_display=[field.name for field in FeatureCollection._meta.get_fields() if not field.many_to_many]
      
admin.site.register(Category, CategoryAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(FeatureCollection, FeatureCollectionAdmin)


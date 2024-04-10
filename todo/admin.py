from django.contrib import admin
from todo.models import Task
from user.models import User
# from geospatial.models import GeoSpatialData
from geospatial.models import GeoSpatialData, PalikaUpload, PalikaGeometry, JsonGeometry, BankGeometry
# from geospatial.models import GeoSpatialDataTranslate
# from modeltranslation.translator import TranslationOptions, register

# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'title','description', 'is_completed','is_created','category']
    list_filter= ("category", "is_completed") 
    search_fields=['title']

class UserAuthAdmin(admin.ModelAdmin):
    list_display=['id', 'username', 'password']    

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


admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAuthAdmin)
admin.site.register(GeoSpatialData, GeoSpatialDataAdmin)
admin.site.register(PalikaUpload, PalikaUploadAdmin)
admin.site.register(PalikaGeometry, PalikaGeometryAdmin)
admin.site.register(JsonGeometry, JsonGeometryAdmin)
admin.site.register(BankGeometry, BankGeometryAdmin)

    
admin.site.site_header = "Todo List Panel"
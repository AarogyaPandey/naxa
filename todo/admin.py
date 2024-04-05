from django.contrib import admin
from todo.models import Task
from user.models import User
# from geospatial.models import GeoSpatialData
from geospatial.models import GeoSpatialData
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
    list_display=['user', 'name', 'description', 'file_type', 'upload_date', 'data_file']
    
# class GeoSpatialDataTranslateAdmin(admin.ModelAdmin):
#     # list_display=['name', 'description']
#     pass

admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAuthAdmin)
admin.site.register(GeoSpatialData, GeoSpatialDataAdmin)
# admin.site.register( GeoSpatialDataTranslate, GeoSpatialDataTranslateAdmin)

    
admin.site.site_header = "Todo List Panel"
from django.contrib import admin
from .models import Task
from user.models import User
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'title','description', 'is_completed','is_created','category']
    list_filter= ("category", "is_completed") 
    search_fields=['title']

class UserAuthAdmin(admin.ModelAdmin):
    list_display=['id', 'username', 'password']    
admin.site.register(Task, TaskAdmin)
admin.site.register(User, UserAuthAdmin)

    
admin.site.site_header = "Todo List Panel"
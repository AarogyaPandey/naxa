from django.contrib import admin
from .models import Task
# Register your models here.

class TaskAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'title','description', 'is_completed','is_created','category']
    list_filter= ("category", "is_completed") 
    search_fields=['title']
    
admin.site.register(Task, TaskAdmin)
    
admin.site.site_header = "Todo List Panel"
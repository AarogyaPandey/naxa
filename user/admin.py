from django.contrib import admin
from user.models import User

class UserAuthAdmin(admin.ModelAdmin):
    list_display=['id', 'username', 'password']
    
admin.site.register(User, UserAuthAdmin)

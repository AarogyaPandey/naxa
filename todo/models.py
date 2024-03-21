from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    '''
    This class represents a task with the attributes given below.
    1. title= string representation
    2. description=optional field but a textfield
    3. complete=boolean field to mark if the task is completed or not
    4. created=inbuilt timestamp is created  when object is called
    '''
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=100)
    description=models.TextField(null=True, blank=True)
    complete=models.BooleanField(default=False)
    created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        '''
        This func is for the string representation. It returns the title of the task.
        '''
        return self.title
    
    class Meta:
        '''
        This class contains additional info of model (Task).
        '''
        ordering=['complete']
from django.db import models
from django.contrib.auth.models import User

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
    is_completed=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True)
    due_date=models.DateTimeField(blank=True, null=True) 
    estimated_hours=models.FloatField(default=0) #this will be used for time tracking 
    
    
    class Category(models.TextChoices):
        """
        This  class contains different categories of tasks that can be assigned.
        """
        WORK= "WK", "Work"
        PERSONAL= "PRSNL", "Personal"
        STUDY= "STDY", "Study"
        HEALTH= "HLT", "Health"
        FINANCE= "FNS", "Finance"
        HOME= "HM" , "Home"
        SOCIAL= "SCL", "Social"
        SHOPPING= "SPNG","Shopping"
        ENTERTAINMENT= "ENTNT" ,"Entertainment"
        
    category=models.CharField( 
        max_length=5,
        choices=Category.choices,
        default=Category.WORK,
    )
    
    
    def __str__(self):
        '''
        This func is for the string representation. It returns the title of the task.
        '''
        return self.title
    
    
    class Meta:
        '''
        This class contains additional info of model (Task).
        '''
        ordering=['is_completed']
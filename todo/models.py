from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gismd

class Task(models.Model):
    '''
    This class represents a task with the attributes given below.
    1. title= string representation
    2. description=optional field but a textfield
    3. complete=boolean field to mark if the task is completed or not
    4. created=inbuilt timestamp is created  when object is called
    '''
    
    STATUS_CHOICES=(
        ("personal","Personal"),
        ("work","Work"),
        ("study", "Study"),
        ("health", "Health"),
        ("finance",  "Finance"),
        ("home", "Home"),
        ("social", "Social"),
        ("shopping", "Shopping"),
        ("entertainment", "Entertainment"),
        ("n/a", "N/A"),
    )
    user=models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=100, null=True, blank=True)
    description=models.TextField(null=True, blank=True, max_length=1000)
    is_completed=models.BooleanField(default=False)
    is_created=models.DateTimeField(auto_now_add=True)
    due_date=models.DateTimeField(blank=True, null=True) 
    location=gismd.GeometryField(null=True, blank=True)
    estimated_hours=models.CharField(max_length=50, blank=True, null=True)  
    category=models.CharField( 
        max_length=15,
        choices=STATUS_CHOICES,
        default="N/A",
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
        
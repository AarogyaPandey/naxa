
from rest_framework import  serializers
from todo.models import Task


class TaskSerializer(serializers.ModelSerializer):
    '''
    This class  is a serializer for the Task model in our app.
    '''
    class Meta:
        '''
        This class  contains additional information about the fields of this serializer.
        '''
        model=Task
        fields = ('id','user', 'title','description', 'is_completed','location','is_created', 'due_date', 'estimated_hours','category')
    

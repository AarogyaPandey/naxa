
from rest_framework import  serializers
from .models import Task
import django_filters


class TaskSerializer(serializers.ModelSerializer):
    '''
    This class  is a serializer for the Task model in our app.
    '''
    class Meta:
        '''
        This class  contains additional information about the fields of this serializer.
        '''
        model=Task
        fields = ('id','user', 'title','description', 'is_completed','is_created', 'due_date', 'estimated_hours','category')
        
        
    # def create(self,  validated_data):
    #     """
    #     This  method overrides the default `create` method of the serializer to add extra functionality.
    #     """
    #     return  Task.objects.create(**validated_data)
    
    
    # def update(self, instance, validated_data):
    #     """
    #     This   method overrides the default `update` method of the serializer to add extra functionality.
    #     """
    #     instance.title=validated_data.get('title', instance.title)
    #     instance.description=validated_data.get('description', instance.description)
    #     instance.is_completed=validated_data.get('is_completed', instance.is_completed)
    #     instance.is_created=validated_data.get('is_created', instance.is_created)
    #     instance.due_date=validated_data.get('due_date', instance.due_date)
    #     instance.estimated_hours=validated_data.get('estimated_hours', instance.estimated_hours)
    #     instance.save()
    #     return instance
    
    
class TaskFilter(django_filters.FilterSet):
    """
    This  class represents a custom filterset that will be used and the filter is based on the `category` of Task Model.
    """
    category=django_filters.CharFilter(field_name="category")
    estimated_hours=django_filters.NumberFilter(field_name="estimated_hours")
    title=django_filters.CharFilter(field_name="title",lookup_expr="icontains")
    description = django_filters.CharFilter(field_name="description")
    
    
    class Meta:
        """
        This class contains the additional information about filter and the field for the filter.
        """
        model= Task
        fields=['title']
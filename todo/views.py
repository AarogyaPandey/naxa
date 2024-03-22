from django.shortcuts import render
from .serializers import TaskSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Task
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
# from rest_framework.pagination import CustomPageNumberPagination

class MyPagination(PageNumberPagination):
    # pagination_class= PageNumberPagination
    page_size=2
    page_size_query_param='page_size'
    max_page_size=2
        
class TodoViewSet(viewsets.ModelViewSet):
    '''
    this class  defines the create, read, update and delete functionality.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class=MyPagination
    
    def list(self, request, *args, **kwargs):
        '''
        this func deals with the filter if the  user wants to get all tasks or only completed ones.
        pagination..
        '''
        completed = self.request.query_params.get("completed", None)
        # completed = self.request.data.get( "completed", "true" )
        if completed == "yes":
            self.queryset = Task.objects.filter(complete = True)
        else:
            self.queryset = Task.objects.all() 
        return super().list(request,*args,**kwargs)
    
    def destroy(self, request, *args, **kwargs):
        '''
        It is a func  that handles deleting an object
        '''
        instance = self.get_object()
        instance.delete()
        return Response({f"message": f"Object with id {instance.id} deleted"}, status=status.HTTP_204_NO_CONTENT)
    

    
    
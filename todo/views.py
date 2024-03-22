from django.shortcuts import render
from .serializers import TaskSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Task
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from .serializers import TaskFilter
from django_filters.rest_framework import  DjangoFilterBackend


class MyPagination(PageNumberPagination):
    """
    This class  is used to set the pagination scheme for our API.
    """
    page_size=5
    page_size_query_param='page_size'
    max_page_size=2
        
        
class TodoViewSet(viewsets.ModelViewSet):
    '''
    this class  defines the create, read, update and delete functionality.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class=MyPagination
    filter_backends= [DjangoFilterBackend]
    filterset_class=TaskFilter
    
    
    def list(self, request, *args, **kwargs):
        '''
        this func deals with the filter if the  user wants to get all tasks or only completed ones.
        
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
    
    
    def  task_list(request):
        """
        This method  returns a list of all the tasks in the database.
        """
        if request.method=='GET':
            task=Task.objects.all()
            serializer= TaskSerializer(task,many=True)
            return JsonResponse(serializer.data, safe=False)
        
        elif request.method=='POST':
            data=JSONParser().parse(request)
            serializer=TaskSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)
        
        
    def task_detail(request,pk):
        """
        This  method returns details about a particular task such as title , description and completion status.
        Retrieve, update or delete a code snippet instance.
        """
        try:
            task=Task.objects.get(pk=pk)
        except task.DoesNotExist:
            return HttpResponse(status=404)  
        
        if request.method=='GET':
            serializer=TaskSerializer(task)
            return JsonResponse(serializer.data)
        
        elif request.method=='PUT':
            data=JSONParser().parse(request)
            serializer=TaskSerializer(task,data=data)

            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data)
            return JsonResponse(serializer.errors, status=400)
        
        elif request.method=='DELETE':
            task.delete()
            return HttpResponse(status=204)
        
    
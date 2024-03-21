from django.shortcuts import render
from .serializers import TaskSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Task
from rest_framework.response import Response

class TodoViewSet(viewsets.ModelViewSet):
    '''
    this class  defines the create, read, update and delete functionality.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
   
    
    def list(self, request, *args, **kwargs):
        '''
        this func deals with the filter if the  user wants to get all tasks or only completed ones.
        '''
        completed = self.request.query_params.get("completed", None)
        print('hello', completed)
        # completed = self.request.data.get( "completed", "true" )
        if completed == "yes":
            queryset = Task.objects.filter(complete = True)
        else:
            queryset = Task.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response({"result":serializer.data})
    
    def destroy(self, request, *args, **kwargs):
        '''
        It is a func  that handles deleting an object
        '''
        instance = self.get_object()
        instance.delete()
        return Response({f"message": f"Object with id {instance.id} deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
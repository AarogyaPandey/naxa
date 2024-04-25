from django.shortcuts import render
from .serializers import TaskSerializer
from rest_framework import viewsets, status, filters
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from todo.filters import TaskFilter
from django_filters.rest_framework import  DjangoFilterBackend
from .pagination import MyPagination
from django.views.decorators.csrf import  csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, authentication_classes


from todo.models import Task
        
class TodoViewSet(viewsets.ModelViewSet):
    '''
    this class  defines the create, read, update and delete functionality.
    '''
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class=MyPagination
    filter_backends= [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class=TaskFilter
    search_fields=['title', 'category','estimated_hours']
    ordering_fields= ['id', 'category', 'title']
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]
    
    
    #-----------the below code is  for customizing response using the modelviewset ---------------

    def list(self, request, *args, **kwargs):
        '''
        this func deals with the filter if the  user wants to get all tasks or only completed ones.
        
        '''
        completed = self.request.query_params.get("completed", None)
        if completed == "True":
            self.queryset = Task.objects.filter(complete = True)
        else:
            self.queryset = Task.objects.all() 
        return super().list(request,*args,**kwargs)
    
    def  retrieve(self, request, *args, **kwargs):
        """
        Returns the specified task instance.
        """
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        data = serializer.data
        return Response(data)
    
    def create(self, request, *args, **kwargs):
        '''
        This function adds a new task in the database.
        '''
        serializer=TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def destroy(self, request, *args, **kwargs):
        '''
        It is a func  that handles deleting an object
        '''
        instance = self.get_object()
        instance_id=instance.id
        instance.delete()
        return Response({f"message": f"Object with id {instance_id} deleted"}, status=status.HTTP_204_NO_CONTENT)
    #--------------------------------------------------------------------------------------------------------------------
    
    
    #------------------------------using decorater and function based api--------------------------------------
@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def  task_list(request):
    """
    This method  returns a list of all the tasks in the database.
    """
    category_name=request.query_params.get("category", None)
    paginator=MyPagination()
    if request.method=='GET':
        task=Task.objects.all(category=category_name)
        result=paginator.paginate_queryset(task,request)
        serializer= TaskSerializer(result,many=True)
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method=='POST':
        data=JSONParser().parse(request)
        serializer=TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
        
@csrf_exempt      
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

    
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])    
@api_view(['GET'])
def todo_details(request): 
    '''
    This function  is used to get all the tasks of user which is based in category.
    '''
    category_name=request.query_params.get("category", None)
    paginator=MyPagination()
    if category_name:
        try:
            task=Task.objects.filter(category=category_name)
            result_page=paginator.paginate_queryset(task,request)
            serializer =TaskSerializer(result_page,many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception  as e :
            return Response(f"Error: {str(e)}", status=404)
    else:
        return Response("category_name is required", status=400)


@csrf_exempt
@api_view(["POST"])
def todo_post(request): 
    '''
    This function is for the POST request.
    '''
    obj_post=TaskSerializer(data=request.data)
    if obj_post.is_valid():
        obj_post.save()
        return Response(obj_post.data, status=201)
        
        #----------------------Class Based API---------------------------
        
class TodoDetails(APIView):
    """
    This class  is used to handle HTTP GET requests

    """
    authentication_classes=[TokenAuthentication] 
    permission_classes=[IsAuthenticated]
    def get(self, request):
        category_name=request.query_params.get('category',None)
        paginator=MyPagination()
        if category_name:
            try:
                tasks=Task.objects.filter(category=category_name)
                result_page=paginator.paginate_queryset(tasks,request)
                serializer=TaskSerializer(result_page,many=True)
                return paginator.get_paginated_response(serializer.data)
            except Exception as e:
                return Response("Error Occurred : "+str(e),status=404)
        else:
            tasks=Task.objects.all()
            serializer=TaskSerializer(tasks, many=True)
            return Response(serializer.data,status=200)
        
class TodoPost(APIView):
    '''
    This class  is used to handle HTTP POST. It validates data and save it into database.
    '''
    def post(self,request,pk):
        task = Task.objects.filter(id=pk)  
        if not task:
            return Response({"error":"Invalid ID"},status=404)
        else:
            data=request.data
            serializer=TaskSerializer(instance=task,data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
            
class TodoDelete(APIView):
    '''
    This  class is used for handling Http DELETE Requests.It deletes the object based on given id.
    '''
    def  delete(self,request,pk):
        task=Task.objects.filter(id=pk).delete()
        if task:
            return Response("deleted", status=204)
        else:
            return Response({"error"}, status=404)
        
class TodoPatch(APIView):
    '''
    This class  handles HTTP PATCH requests. It updates a particular field in the database.
    '''
    def  patch(self, request, pk):
        task = Task.objects.get(id=pk)
        data = {'is_completed': True}
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
        
        
class TodoPut(APIView):
    '''
    This class  handles HTTP Put requests which update an instance of Task model.
    '''
    def put(self, request, pk):
        try:
            task=Task.objects.get(id=pk)
        except Exception as e:
            return Response(str(e),status=404)
        serializer=TaskSerializer(task,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
            
 
            
                
            
        
    
from django.shortcuts import render
# from django.views.generic.list import ListView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView

from .serializers import TaskSerializer
from rest_framework import viewsets, status
from django.http import JsonResponse
from .models import Task
from rest_framework.response import Response
# Create your views here.

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # return JsonResponse(serializer.data)
    # return  HttpResponse("Hello")
    
    def list(self, request, *args, **kwargs):
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
        instance = self.get_object()
        instance.delete()
        return Response({f"message": f"Object with id {instance.id} deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
    
    
    
# class CustomLoginView(LoginView):
#     template_name='todo/login.html'
#     fields='__all__'
#     redirect_authenticated_user=True
    
#     def get_success_url(self):
#         return reverse_lazy('tasks')
    
    
# class TaskList(ListView):
#     model= Task
#     context_object_name='tasks'
    
# class TaskDetail(DetailView):
#     model=Task
#     context_object_name='task'
    
# class TaskCreate(CreateView):
#     model=Task
#     fields='__all__'
#     success_url=reverse_lazy('tasks') #redirecting user to tasks
    
# class TaskUpdate(UpdateView):
#     model=Task
#     fields='__all__'
#     success_url=reverse_lazy('tasks')
    
# class DeleteView(DeleteView):
#     model=Task
#     context_object_name= 'task'
#     success_url=reverse_lazy('tasks')
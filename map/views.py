from django.shortcuts import render
from rest_framework import viewsets
from map.serializers import LayerSerializer
from django.core.serializers import serialize
from map.models import Layer
from rest_framework import filters
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.response import Response
from map.tasks import process_layer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from map.models import Category
from rest_framework.views import APIView

class LayerViewSet(viewsets.ModelViewSet):
    queryset = Layer.objects.all()
    serializer_class =LayerSerializer
    filter_backends=(
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    )
    search_fields=[
        "layer_name_en",
    ]
    ordering_fields=[]
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    
    def list(self,  request, *args, **kwargs):
        return super().list(request,*args,**kwargs)
    
    def create(self, request, *args, **kwargs):
        serializer=LayerSerializer(data=request.data)
        if serializer.is_valid():
            layer_object=serializer.save(created_by=request.user)
          
        else:
            return Response(serializer.errors)
        
        category = request.data.get('category')
      
        file_upload=request.data.get('file_upload')
        if file_upload:
            layer_id=serializer.data.get('id')
            
            try:
                user_id=request.user.id
                response = process_layer(layer_id, user_id, category)
                
                return Response(
                    {
                        "message":"success",
                        "details":"File upload is in progress",
                        
                },
                status=201,
                )
            except Exception as e:
                return Response(
                    {
                        "message":"error",
                        "details":str(e),
                    },
                    status=400,
                )
        return Response(
    {
        "message": "success",
        "details": "Layer created successfully",
        "layer_id": layer_object.id,
        "category_id": category.id,
    },
    status=400,
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)                            
            
class GetApi(APIView):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category_data = []
        for category in categories:
            category_data.append({
                'id': category.id,
                'name': category.name_en
            })
        
        layers = Layer.objects.all()
        layer_data = []
        for layer in layers:
            layer_data.append({
                'id': layer.id,
                'name': layer.layer_name_en
            })
        
        return Response({
            'categories': category_data,
            'layers': layer_data
        })
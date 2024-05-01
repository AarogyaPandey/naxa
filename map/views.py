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
            print(layer_object.__dict__)
        else:
            return Response(serializer.errors)
        
        category = request.data.get('category')
        print('category', category)   
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
                        # "layer_id":layer_id,
                        # "category_id":category,
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
            
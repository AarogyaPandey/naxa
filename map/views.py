from django.shortcuts import render
from rest_framework import viewsets
from map.serializers import LayerSerializer, FeatureColletionSerializer
from django.core.serializers import serialize
from map.models import Layer
from rest_framework import filters
from django_filters.rest_framework import  DjangoFilterBackend
from rest_framework.response import Response
from map.tasks import process_layer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from map.models import Category, FeatureCollection
from rest_framework.views import APIView
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.gis.geos import GEOSGeometry
import json
from rest_framework.decorators import api_view
from django.http import HttpResponse
import csv
from map.models import CsvUpload
from map.serializers import CsvSerializer      
from django.http import HttpResponse
from map.serializers import CsvSerializer

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
class GetLayer(APIView):
    def get(self, request, *args, **kwargs):
        layer_id = request.query_params.get('layer_id')
        if not layer_id:
            return JsonResponse({
                'message': 'error',
                'details': 'Layer ID is required'
            }, status=400)
        
        try:
            query = FeatureCollection.objects.filter(id=layer_id)
            if not query.exists():
                return JsonResponse({
                    'message': 'error',
                    'details': 'Layer not found'
                }, status=404)
            
            data = serialize('geojson', query, geometry_field="geom")
            data = json.loads(data)
            return JsonResponse(data, content_type='application/json')
        
        except Exception as e:
            return JsonResponse({
                'message': 'error',
                'details': str(e)
            }, status=500)
            
def upload_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        
        if not csv_file.name.endswith('.csv'):
            return HttpResponse("Please upload a CSV file") 
        
        try:
            serializer = CsvSerializer(data=request.POST)
            if serializer.is_valid():
                obj = serializer.save()
                
                obj.file_upload = csv_file
                obj.save()
                
                with open('media/' + csv_file.name, 'wb') as file:
                    for chunk in csv_file.chunks():
                        file.write(chunk)
                
                return HttpResponse("CSV file uploaded successfully")
            
            return HttpResponse("Invalid serializer data")
        
        except Exception as e:
            return HttpResponse("CSV file error: {}".format(e))
    
    return HttpResponse("Please upload a CSV file")
    
# @api_view(["GET"])
# def download_csv(request):
#     query = CsvUpload.objects.all()
#     csv_data = serialize('csv', query)
#     response = HttpResponse(csv_data, content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="data.csv"'
#     return response

@api_view(["GET"])
def download_csv(request):
    query = CsvUpload.objects.all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'
    writer = csv.writer(response)
    for obj in query:
        writer.writerow([obj.file_upload, obj.layer, obj.error])  
    return response

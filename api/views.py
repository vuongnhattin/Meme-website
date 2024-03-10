from django.shortcuts import render
from django.http import HttpResponse, FileResponse, HttpResponseBadRequest, JsonResponse
from rest_framework import generics, mixins, status, viewsets
from rest_framework.response import Response
from .serializers import *
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
import os, json, zipfile
from django.conf import settings
from rest_framework.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

def isInGroup(user, group_name):
    return user.groups.filter(name=group_name).exists()

class IsManager(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.groups.filter(name="Manager").exists()
    
class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        return request.user.groups.filter(name="Customer").exists()

# Create your views here.
class ItemView(generics.ListCreateAPIView):
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        if isInGroup(self.request.user, 'Manager'):
            queryset = Item.objects.all().order_by('id')
            approved = self.request.query_params.get('approved')

            if approved:
                if approved == 'true':
                    queryset = queryset.filter(approved=True)
                elif approved == 'false':
                    queryset = queryset.filter(approved=False)
                else: 
                    queryset = Item.objects.none()
            
            return queryset
        
        return Item.objects.filter(approved=True)

    def perform_create(self, serializer):
        if isInGroup(self.request.user, 'Customer'):
            serializer.validated_data['approved'] = False
        serializer.save()
    
class SingleItemView(generics.RetrieveUpdateDestroyAPIView, generics.CreateAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsManager()]
        if self.request.method in ['POST', 'GET']:
            return [IsAuthenticated()]
        return [IsAuthenticated()]
    
    def create(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        try:
            obj = Cart.objects.create(item=item, user=request.user)
            json_data = json.loads(json.dumps(CartSerializer(obj, context={'request': request}).data))
            return Response(json_data)
        except:
            return Response({'detail': 'You\'ve already added this item'}, status.HTTP_400_BAD_REQUEST)
    
    def perform_destroy(self, instance):
        file_path = instance.image.path
        if os.path.exists(file_path):
            os.remove(file_path)
        
        instance.delete()
        
class CartView(generics.ListAPIView, generics.DestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user.id)
    
    def destroy(self, request):
        Cart.objects.filter(user_id=request.user.id).delete()
        return Response({'detail': 'Removed the whole cart'})

class SingleCartView(generics.RetrieveDestroyAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user_id=self.request.user.id)

    def destroy(self, request, pk):
        Cart.objects.filter(user_id=request.user.id, pk=pk).delete()
        return Response({'detail': 'Removed the current item from the cart'})


@api_view()
def download_single_file(request, pk):
    try:
        item = Item.objects.get(pk=pk)
    except:
        return Response({'detail': 'Request file does not exist'}, status.HTTP_404_NOT_FOUND)

    file_path = item.image.path

    response = FileResponse(open(file_path, 'rb'))

    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{item.image.name}"'

    return response

@api_view()
def download_multiple_files(request):
    user_id = request.user.id
    cart_items = Cart.objects.filter(user_id=user_id)

    if not cart_items.exists():
        return Response({'detail': 'Cart is empty'}, status.HTTP_400_BAD_REQUEST)
    
    # Create a temporary directory to store files to be zipped
    temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp_zip')
    os.makedirs(temp_dir, exist_ok=True)

    file_paths = [obj.item.image.path for obj in cart_items]

    # Create the zip file
    zip_file_path = os.path.join(temp_dir, 'archive.zip')
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        for file_path in file_paths:
            # Add each file to the zip archive
            file_name = os.path.basename(file_path)
            zipf.write(file_path, arcname=file_name)

    # Serve the zip file for download
    response = FileResponse(open(zip_file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename="archive.zip"'
    return response

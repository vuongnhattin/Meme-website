from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['last_name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        ordering = ['id']

class CartSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = Cart
        fields = ['id', 'item']

from dataclasses import fields
from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    """Serializer class of model Item"""
    class Meta:
        model = Item
        fields = '__all__'

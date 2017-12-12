from rest_framework import serializers
from .models import Condition, Entry

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('description', 'serial', 'condition', 'lane', 'ulid', 'series', 'created_at')
        
class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('ulid', 'item', 'value', 'text', 'unit', 'index', 'created_at')
        
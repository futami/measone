from rest_framework import serializers
from .models import Condition, Entry

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('description', 'serial', 'condition', 'lane', 'uuid', 'series', 'created_at')
        
class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('uuid', 'item', 'value', 'text', 'unit', 'index', 'created_at')
        
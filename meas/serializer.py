from rest_framework import serializers
from .models import Condition, Entry

class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condition
        fields = ('description', 'condition', 'created_at', 'lane', 'uuid')
        
class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entry
        fields = ('item', 'value', 'unit', 'uuid')
        
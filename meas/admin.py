from django.contrib import admin

# Register your models here.
from .models import Condition, Entry

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display =('description', 'serial', 'condition', 'lane', 'series', 'created_at')
    list_filter = ['created_at']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display =('item', 'value', 'unit', 'created_at')
    list_filter = ['item']


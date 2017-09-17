from django.contrib import admin

# Register your models here.
from .models import Condition, Entry

@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display =('description', 'condition', 'lane', 'created_at')
    list_filter = ['created_at']

@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display =('item', 'value', 'unit')
    list_filter = ['item']


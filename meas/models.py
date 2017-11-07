from django.db import models

# Create your models here.
import uuid

class Condition(models.Model):
    description = models.CharField(max_length=256)
    serial = models.CharField(max_length=256, blank=True)
    condition = models.CharField(max_length=256)
    lane = models.IntegerField(default=999, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    series = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

class Entry(models.Model):
    uuid = models.ForeignKey('Condition', to_field='uuid')
    item = models.CharField(max_length=64)
    value = models.FloatField()
    unit = models.CharField(max_length=16, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "entries"
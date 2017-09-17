from django.db import models

# Create your models here.
import uuid

class Condition(models.Model):
    description = models.CharField(max_length=256)
    condition = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    lane = models.IntegerField(blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)

class Entry(models.Model):
    uuid = models.ForeignKey('Condition', to_field='uuid')
    item = models.CharField(max_length=64)
    value = models.FloatField()
    unit = models.CharField(max_length=16, blank=True)
    class Meta:
        verbose_name_plural = "entries"
from django.db import models

# Create your models here.

class Condition(models.Model):
    description = models.CharField(max_length=256)
    serial = models.CharField(max_length=256, blank=True)
    condition = models.CharField(max_length=256)
    lane = models.IntegerField(default=999, blank=True)
    ulid = models.CharField(max_length=30, unique=True)
    series = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)

class Entry(models.Model):
    ulid = models.ForeignKey('Condition', to_field='ulid')
    item = models.CharField(max_length=64)
    value = models.FloatField(null=True, blank=True)
    text = models.CharField(default='', max_length=256)
    unit = models.CharField(max_length=16, blank=True)
    index = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "entries"

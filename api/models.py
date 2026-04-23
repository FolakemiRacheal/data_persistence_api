import uuid6
from django.db import models

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid6.uuid7, editable=False)
    name = models.CharField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, db_index=True)
    gender_probability = models.FloatField()
    sample_size = models.IntegerField()
    age = models.IntegerField(db_index=True)
    age_group = models.CharField(max_length=20, db_index=True)
    country_id = models.CharField(max_length=10, db_index=True)
    country_name = models.CharField(max_length=100,null=True,blank=True)
    country_probability = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
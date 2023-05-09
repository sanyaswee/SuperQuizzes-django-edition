from django.db import models


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_age = models.SmallIntegerField(max_length=3)
    max_age = models.SmallIntegerField(max_length=3)
    tags = models.TextField()

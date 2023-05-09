from django.db import models


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_age = models.SmallIntegerField()
    max_age = models.SmallIntegerField(default=100)
    tags = models.TextField()

    completed_as_form = models.IntegerField(default=0)
    completed_as_quiz = models.IntegerField(default=0)

    available = models.BooleanField(default=False)

    def __str__(self):
        return self.name

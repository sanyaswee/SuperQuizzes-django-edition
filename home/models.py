from django.db import models


# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_age = models.SmallIntegerField()
    max_age = models.SmallIntegerField(default=100)
    tags = models.TextField()

    completed_as_form = models.IntegerField(default=0)
    completed_as_quiz = models.IntegerField(default=0)
    average_score = models.IntegerField(default=0)

    available = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.id}: {self.name}'


class Question(models.Model):
    question = models.CharField(max_length=200)

    right_answer = models.CharField(max_length=50)
    wrong_answer1 = models.CharField(max_length=50)
    wrong_answer2 = models.CharField(max_length=50)
    wrong_answer3 = models.CharField(max_length=50)

    answers_amount = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

    def __str__(self):
        return f'#{self.id}: {self.question}'

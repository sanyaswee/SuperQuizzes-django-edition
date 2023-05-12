from django.db import models


# Create your models here.


class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    popular = models.BooleanField()

    def __str__(self):
        return self.tag


class Question(models.Model):
    question = models.CharField(max_length=200, unique=True)

    right_answer = models.CharField(max_length=100)
    wrong_answer1 = models.CharField(max_length=100)
    wrong_answer2 = models.CharField(max_length=100)
    wrong_answer3 = models.CharField(max_length=100)

    answers_amount = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)

    def __str__(self):
        return f'#{self.id}: {self.question}'


class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_age = models.SmallIntegerField()
    max_age = models.SmallIntegerField(default=100)
    tags = models.TextField()
    questions = models.ManyToManyField(Question, related_name='quizzes')

    completed_as_form = models.IntegerField(default=0)
    completed_as_quiz = models.IntegerField(default=0)
    average_score = models.IntegerField(default=0)

    available = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.id}: {self.name}'

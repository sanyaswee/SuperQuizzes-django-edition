from django.db import models
from django.conf import settings


# Create your models here.


class Tag(models.Model):
    tag = models.CharField(max_length=20, unique=True)
    localized_uk_ua = models.CharField(max_length=20, unique=True, blank=True)
    popular = models.BooleanField()

    def __str__(self):
        return self.tag


class Question(models.Model):
    question = models.CharField(max_length=200, unique=True)

    right_answer = models.CharField(max_length=100)
    wrong_answer1 = models.CharField(max_length=100)
    wrong_answer2 = models.CharField(max_length=100)
    wrong_answer3 = models.CharField(max_length=100)

    # answers_amount = models.IntegerField(default=0)
    # correct_answers = models.IntegerField(default=0)

    def __str__(self):
        return f'#{self.id}: {self.question}'


class Quiz(models.Model):
    name = models.CharField(max_length=50, unique=True)
    min_age = models.SmallIntegerField()
    max_age = models.SmallIntegerField(default=100)
    tags = models.ManyToManyField(Tag, related_name='quizzes')
    questions = models.ManyToManyField(Question, related_name='quizzes')

    # completed_as_form = models.IntegerField(default=0)
    # completed_as_quiz = models.IntegerField(default=0)
    # average_score = models.IntegerField(default=0)

    available = models.BooleanField(default=False)

    def __str__(self):
        return f'#{self.id}: {self.name}'


class Completion(models.Model):  # Instead of 'Quiz.completed_as_...' and 'Quiz.average_score'
    # General quiz info
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='completions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='completions', null=True
    )
    is_form = models.BooleanField()  # Instead of 'completion_type' filed. True = form, False = quiz

    # Time info
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(auto_now=True)

    # Results info
    right_answers = models.IntegerField()
    score = models.IntegerField()


class UserAnswer(models.Model):
    completion = models.ForeignKey(Completion, on_delete=models.CASCADE, related_name='answers')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='quiz_answers', null=True
    )

    right = models.BooleanField()

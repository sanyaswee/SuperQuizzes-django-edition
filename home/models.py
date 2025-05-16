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
    searchable = models.CharField(max_length=50, null=True)  # = name.lower()
    min_age = models.SmallIntegerField()
    max_age = models.SmallIntegerField(default=100)
    tags = models.ManyToManyField(Tag, related_name='quizzes')
    questions = models.ManyToManyField(Question, related_name='quizzes')

    available = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Save searchable
        self.searchable = self.name.lower()
        super(Quiz, self).save(*args, **kwargs)

    def __str__(self):
        return f'#{self.id}: {self.name}'

    def __lt__(self, other):
        return self.name < other.name


class Completion(models.Model):  # Instead of 'Quiz.completed_as_...' and 'Quiz.average_score'
    # General quiz info
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='completions')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='completions', null=True
    )
    is_form = models.BooleanField()  # Instead of 'completion_type' filed. True = form, False = quiz
    token = models.CharField(unique=True, max_length=64)

    # Time info
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(auto_now_add=True)

    # Results info
    score = models.FloatField(default=0)


class UserAnswer(models.Model):
    completion = models.ForeignKey(Completion, on_delete=models.CASCADE, related_name='answers')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='user_answers')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='quiz_answers', null=True
    )

    right = models.BooleanField()

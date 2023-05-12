from django.contrib import admin
from .models import Quiz, Question


# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'tags', 'available']
    list_display_links = ['name']
    search_fields = ['name', 'tags']

    fields = ['name', 'min_age', 'max_age', 'tags', 'available', 'questions']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']
    list_display_links = ['question']
    search_fields = ['question', 'quiz']

    fields = ['question', 'right_answer', 'wrong_answer1', 'wrong_answer2', 'wrong_answer3']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)

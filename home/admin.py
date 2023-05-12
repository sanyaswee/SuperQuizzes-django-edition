from django.contrib import admin
from .models import Quiz, Question, Tag


# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'available']
    list_display_links = ['name']
    search_fields = ['name', 'tags']

    fields = ['name', 'min_age', 'max_age', 'tags', 'available', 'questions']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question']
    list_display_links = ['question']
    search_fields = ['question', 'quiz']

    fields = ['question', 'right_answer', 'wrong_answer1', 'wrong_answer2', 'wrong_answer3']


class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag', 'localized_uk_ua', 'popular']
    list_display_links = ['tag']
    search_fields = ['tag', 'localized_uk_ua']


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Tag, TagAdmin)

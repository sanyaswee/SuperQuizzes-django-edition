from django.contrib import admin
from .models import Quiz


# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name', 'tags', 'available']
    list_display_links = ['name']
    search_fields = ['name', 'tags']

    fields = ['name', 'min_age', 'max_age', 'tags', 'available']


admin.site.register(Quiz, QuizAdmin)

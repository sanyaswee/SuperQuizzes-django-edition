from django.contrib import admin
from .models import Quiz


# Register your models here.
class QuizAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_display_links = ['name']
    search_fields = ['name']


admin.site.register(Quiz, QuizAdmin)

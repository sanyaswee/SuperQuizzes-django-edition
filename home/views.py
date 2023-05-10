from django.shortcuts import render
from .models import Quiz


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(available=True)

    return render(request, 'home/quiz_list.html', {'quizzes': quizzes})

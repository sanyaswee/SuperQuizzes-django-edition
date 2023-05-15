from django.shortcuts import render
from .models import Quiz


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(available=True)

    color_classes = ['red-box', 'yellow-box', 'blue-box', 'green-box']

    return render(request, 'home/quiz_list.html', {'quizzes': quizzes, 'color_classes': color_classes})

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .models import Quiz


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(available=True)

    color_classes = ['red-box', 'yellow-box', 'blue-box', 'green-box']

    return render(request, 'home/quiz_list.html', {'quizzes': quizzes, 'color_classes': color_classes})


def form(request: HttpRequest):
    form_id = request.GET.get('id', '')
    if form_id:
        quiz = Quiz.objects.get(id=form_id)

        return render(request, 'home/form.html', {'quiz': quiz})
    else:
        return redirect('index')

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
        questions = quiz.questions.all()

        for q in questions:
            q.answers = [q.right_answer, q.wrong_answer1, q.wrong_answer2, q.wrong_answer3]

        return render(request, 'home/form.html', {'quiz_name': quiz.name, 'questions': questions})
    else:
        return redirect('index')

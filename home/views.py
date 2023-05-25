from django.contrib.auth import get_user
from django.db.models import Avg
from django.http import HttpRequest  # , HttpResponse
from django.shortcuts import render, redirect

from . import tools

from .models import Quiz, Question, Completion, UserAnswer, Tag


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(available=True)

    color_classes = ['red-box', 'yellow-box', 'blue-box', 'green-box']

    return render(request, 'home/quiz_list.html', {'quizzes': quizzes, 'color_classes': color_classes})


def form(request: HttpRequest):
    form_id = request.GET.get('id', '')
    if form_id:
        quiz, questions = tools.get_qq(form_id)

        return render(request, 'home/form.html', {'quiz_name': quiz.name, 'quiz_id': quiz.id, 'questions': questions})
    else:
        return redirect('index')


def result(request: HttpRequest):
    if request.method == 'POST':
        quiz, post_copy, completion, user = tools.result_post(request)
        processed_answers = tools.process_answers(post_copy, user, completion, quiz)

        completion = Completion.objects.get(id=completion.id)
        time_taken = completion.end_time - completion.start_time

        # Getting average stats
        completions = Completion.objects.filter(quiz=quiz)
        average_score = round(completions.aggregate(Avg('score'))['score__avg'], 2)

        average_time = tools.get_avg_time(completions)

        params = {
            'time_taken': time_taken.seconds,
            'average_score': average_score,
            'average_time': average_time,
        }

        context = processed_answers | params

        return render(request, 'home/result.html', context)
    else:
        return redirect('index')


def filter_view(request: HttpRequest):
    if request.method == 'GET':
        conditions = {'available': True}
        conditions = tools.search(request, conditions)
        conditions = tools.filter_age(request, conditions)
        conditions = tools.process_tags(request, conditions)

        quizzes = Quiz.objects.filter(**conditions)

        if len(quizzes) == 0:
            return render(request, 'home/nothing_found.html')

        color_classes = ['red-box', 'yellow-box', 'blue-box', 'green-box']
        return render(request, 'home/quiz_list.html', {'quizzes': quizzes, 'color_classes': color_classes})

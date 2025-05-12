from django.db.models import Avg
from django.db.utils import IntegrityError
from django.http import HttpRequest  # , HttpResponse
from django.shortcuts import render, redirect
from django import forms

from . import tools
from .models import Quiz, Completion, Tag
from .templatetags.sort import key as tag_sort_key
from .forms import FilterForm


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(available=True)
    quizzes = sorted(quizzes, key=tools.sort_alphabetically_key)

    tags = Tag.objects.filter(popular=True)
    tag_choices = [(tag.tag, tag.localized_uk_ua) for tag in tags]

    # Dynamically add checkbox fields for tags
    class DynamicFilterForm(FilterForm):
        pass

    for tag_value, tag_label in tag_choices:
        DynamicFilterForm.base_fields[tag_value] = forms.BooleanField(
            label=tag_label, required=False  # No _(tag_label)
        )

    form = DynamicFilterForm(request.GET or None)

    if form.is_valid():
        search = form.cleaned_data.get('search')
        for_age = form.cleaned_data.get('for_age')

        # Filter by name
        if search:
            quizzes = [q for q in quizzes if search.lower() in q.name.lower()]

        # Filter by age
        if for_age:
            quizzes = [q for q in quizzes if q.for_age <= for_age]

        # Filter by tags
        selected_tags = [tag.tag for tag in tags if form.cleaned_data.get(tag.tag)]
        if selected_tags:
            quizzes = [q for q in quizzes if any(tag.tag in selected_tags for tag in q.tags.all())]

    return render(request, 'home/quiz_list.html', {
        'quizzes': quizzes,
        'tags': tags,
        'form': form
    })

def coming_soon(request: HttpRequest):
    return render(request, 'home/soon.html')


def form(request: HttpRequest, id_):
    # form_id = request.GET.get('id', '')
    if id_:
        quiz, questions = tools.get_qq(id_)

        return render(request, 'home/form.html', {'quiz_name': quiz.name, 'quiz_id': quiz.id, 'questions': questions})
    else:
        return redirect('index')


def quiz_view(request: HttpRequest):
    return redirect('soon')


def result(request: HttpRequest):
    if request.method == 'POST':
        try:
            quiz, post_copy, completion, user = tools.result_post(request)
        except IntegrityError:
            processed_answers = tools.get_answers(request)
        else:
            processed_answers = tools.process_answers(post_copy, user, completion, quiz)

        completion = tools.get_completion(request)

        # Getting average stats
        completions = Completion.objects.filter(quiz=completion.quiz)
        average_score = round(completions.aggregate(Avg('score'))['score__avg'], 2)

        average_time = tools.get_avg_time(completions)

        time_taken = completion.end_time - completion.start_time
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
        try:
            conditions = tools.search(request, conditions)
            conditions = tools.filter_age(request, conditions)
            conditions = tools.filter_questions_amount(request, conditions)
            conditions = tools.process_tags(request, conditions)
        except AssertionError:
            return render(request, 'home/filter_error.html')

        quizzes = Quiz.objects.filter(**conditions)
        quizzes = sorted(quizzes, key=tools.sort_alphabetically_key)

        if len(quizzes) == 0:
            return render(request, 'home/nothing_found.html')

        tags = Tag.objects.filter(popular=True)
        return render(
            request, 'home/quiz_list.html', {'quizzes': quizzes, 'tags': tags}
        )


def advanced_search(request: HttpRequest):
    tags = sorted(Tag.objects.all(), key=tag_sort_key)
    tags = tools.convert_tags_to_table(tags)

    return render(request, 'home/advanced_search.html', {'tags': tags})

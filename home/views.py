from django.db.models import Avg
from django.db.utils import IntegrityError
from django.http import HttpRequest  # , HttpResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now

from . import tools
from .forms import FilterForm, AdvancedSearchForm, QuizForm
from .models import Quiz, Completion, Tag
from .templatetags.sort import key as tag_sort_key


# Create your views here.
def index(request):
    quizzes = Quiz.objects.filter(available=True).order_by('name')
    tags = Tag.objects.filter(popular=True)

    return render(request, 'home/quiz_list.html', {
        'quizzes': quizzes,
        'tags': tags,
        'form': FilterForm(tags=tags)
    })


def coming_soon(request: HttpRequest):
    return render(request, 'home/soon.html')


def form(request: HttpRequest, id_):
    if not id_:
        return redirect('index')

    quiz, questions = tools.get_qq(id_)

    # Prepare the form to be POSTed to 'result'
    q_form = QuizForm(questions, initial={
        'quiz_id': quiz.id,
        'start_time': now().isoformat(),
        'completed_as': 'form',
    })

    return render(request, 'home/form.html', {
        'quiz_name': quiz.name,
        'quiz_id': quiz.id,
        'questions': questions,
        'form': q_form,
    })


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

        # Getting other users' results for this quiz
        other_results = Completion.objects.filter(quiz=completion.quiz).order_by('-score', 'end_time')[:10]  # Top 10

        # Format other users' results
        other_users_data = []
        for result in other_results:
            username = result.user.username if result.user else "guest"
            time_taken = (result.end_time - result.start_time).seconds
            other_users_data.append({
                'username': username,
                'score': result.score,
                'time_taken': time_taken,
                'completion_date': result.end_time,
            })

        time_taken = completion.end_time - completion.start_time
        params = {
            'time_taken': time_taken.seconds,
            'average_score': average_score,
            'average_time': average_time,
            'other_users_results': other_users_data,
            'quiz_id': completion.quiz.id
        }

        context = processed_answers | params

        return render(request, 'home/result.html', context)
    else:
        return redirect('index')


def filter_view(request):
    if request.method == 'GET':
        tags = Tag.objects.filter(popular=True)
        filter_form = FilterForm(request.GET or None, tags=tags)

        if not filter_form.is_valid():
            return render(request, 'home/filter_error.html', {'form': filter_form})

        quizzes = Quiz.objects.filter(available=True)

        search = filter_form.cleaned_data.get('search')
        for_age = filter_form.cleaned_data.get('for_age')

        if search:
            quizzes = quizzes.filter(name__icontains=search)
        if for_age:
            quizzes = quizzes.filter(min_age__lte=for_age, max_age__gte=for_age)

        selected_tag_slugs = [tag.tag for tag in tags if filter_form.cleaned_data.get(tag.tag)]
        if selected_tag_slugs:
            quizzes = quizzes.filter(tags__tag__in=selected_tag_slugs).distinct()

        quizzes = quizzes.order_by('name')

        if not quizzes.exists():
            return render(request, 'home/nothing_found.html', {'tags': tags, 'form': filter_form})

        return render(request, 'home/quiz_list.html', {
            'quizzes': quizzes,
            'tags': tags,
            'form': filter_form,
        })

    return redirect('index')


def advanced_search(request: HttpRequest):
    all_tags = sorted(Tag.objects.all(), key=tag_sort_key)
    search_form = AdvancedSearchForm(request.GET or None, tags=all_tags)

    # Optional: format tag fields into a table for display
    tag_table = tools.convert_tags_to_table(all_tags)

    return render(request, 'home/advanced_search.html', {
        'form': search_form,
        'tag_table': tag_table  # only for layout
    })


def all_results(request: HttpRequest, quiz_id):
    try:
        quiz = Quiz.objects.get(id=quiz_id, available=True)
    except Quiz.DoesNotExist:
        return redirect('index')

    # Get all results for this quiz
    all_completions = Completion.objects.filter(quiz=quiz).order_by('-score', 'end_time')

    # Format all users' results
    all_users_data = []
    for result in all_completions:
        username = result.user.username if result.user else "guest"
        time_taken = (result.end_time - result.start_time).seconds
        all_users_data.append({
            'username': username,
            'score': result.score,
            'time_taken': time_taken,
            'completion_date': result.end_time
        })

    # Calculate stats
    average_score = round(all_completions.aggregate(Avg('score'))['score__avg'], 2) if all_completions.exists() else 0
    total_completions = all_completions.count()

    return render(request, 'home/all_results.html', {
        'quiz': quiz,
        'all_results': all_users_data,
        'average_score': average_score,
        'total_completions': total_completions,
    })

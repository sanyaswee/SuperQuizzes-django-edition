from django.contrib.auth import get_user
from django.conf import settings
from django.http import HttpRequest
from django.shortcuts import get_object_or_404
from .models import Quiz, Completion, Question, UserAnswer, Tag


def get_qq(id_):
    """Get quizzes and questions"""
    quiz = get_object_or_404(Quiz, id=id_)
    questions = quiz.questions.all()

    for q in questions:
        q.answers = [q.right_answer, q.wrong_answer1, q.wrong_answer2, q.wrong_answer3]

    return quiz, questions


def result_post(request: HttpRequest):
    """Handle POST request for result"""
    copy = dict(request.POST)
    del copy['csrfmiddlewaretoken']
    quiz = Quiz.objects.get(id=copy.pop('quiz-id')[0])
    is_form = copy.pop('completed-as')[0]

    if is_form == 'form':
        is_form = True
    else:
        is_form = False

    completion, copy, user = _create_completion(request, quiz, is_form, copy, request.POST.get('csrfmiddlewaretoken'))

    return quiz, copy, completion, user


def _create_completion(request: HttpRequest, quiz: Quiz, is_form: bool, post_copy: dict, csrf_token):
    completion = Completion(
        quiz=quiz, is_form=is_form, token=csrf_token, start_time=post_copy.pop('start-time')[0]
    )
    user = get_user(request)
    if not user.is_anonymous:
        completion.user = user
    completion.save()
    return completion, post_copy, user


def _clear_request(request: HttpRequest):
    copy = request.POST.copy()
    del copy['csrfmiddlewaretoken'], copy['quiz-id'], copy['completed-as'], copy['start-time']
    return copy


def process_answers(answers_query: dict, user, completion: Completion, quiz: Quiz):
    """Process user's answers"""
    right_answers, total_questions = 0, 0
    answers = []
    for q, a in answers_query.items():
        db_question = Question.objects.get(question=q)
        answer = [q, a[0], db_question.right_answer]
        user_answer = UserAnswer(completion=completion, quiz=quiz, question=db_question)
        if not user.is_anonymous:
            user_answer.user = user

        if a[0] == db_question.right_answer:
            right_answers += 1
            answer.append('Так')
            user_answer.right = True
        else:
            answer.append('Ні')
            user_answer.right = False

        total_questions += 1
        answers.append(answer)
        user_answer.save()

        answer.append(get_avg_right_answers(db_question))

    score = round(right_answers / total_questions * 100, 2)
    completion.score = score
    completion.save()

    processed = {
                'right_answers': right_answers,
                'total_questions': total_questions,
                'score': score,
                'answers': answers,
            }

    return processed


def get_avg_right_answers(question: Question):
    """Returns % of right answers for given question"""
    return round(len(question.user_answers.filter(right=True)) / len(question.user_answers.all()) * 100, 2)


def get_answers(request: HttpRequest):
    """Returns answers from Completion object"""
    copy = _clear_request(request)
    print(copy)
    right_answers, total_questions = 0, 0
    answers = []
    for q, a in copy.items():
        db_question = Question.objects.get(question=q)
        answer = [q, a, db_question.right_answer]

        if a == db_question.right_answer:
            right_answers += 1
            answer.append('Так')
        else:
            answer.append('Ні')

        answer.append(get_avg_right_answers(db_question))
        total_questions += 1
        answers.append(answer)

    score = round(right_answers / total_questions * 100, 2)
    processed = {
        'right_answers': right_answers,
        'total_questions': total_questions,
        'score': score,
        'answers': answers,
    }
    return processed


def get_avg_time(completions):
    """Calculate average time taken for a quiz"""
    average_time, i = 0, 0
    for c in completions:
        taken = c.end_time - c.start_time
        average_time += taken.seconds
        i += 1

    average_time /= i

    return round(average_time, 2)


def search(request: HttpRequest, conditions: dict):
    """Get search conditions for SQL"""
    search_request = request.GET.get('search')
    if search:
        conditions['searchable__contains'] = search_request.lower()

    return conditions


def filter_age(request: HttpRequest, conditions: dict):
    """Build a conditions for particular age"""
    for_age = request.GET.get('for-age')
    if for_age:
        conditions['min_age__lte'] = for_age
        conditions['max_age__gte'] = for_age

    return conditions


def filter_questions_amount(request: HttpRequest, conditions: dict):
    """Build a conditions for questions amount"""
    min_questions = request.GET.get('min-questions')
    max_questions = request.GET.get('max-questions')
    ids = set()

    greater_than = set()
    if min_questions:
        min_questions = int(min_questions)
        for q in Quiz.objects.all():
            if len(q.questions.all()) >= min_questions:
                greater_than.add(q.id)

    ids = ids.union(greater_than)

    less_than = set()
    if max_questions:
        max_questions = int(max_questions)
        # assert min_questions <= max_questions
        for q in Quiz.objects.all():
            if len(q.questions.all()) <= max_questions:
                less_than.add(q.id)

    if less_than:
        ids.intersection_update(less_than)

    if ids:
        conditions['id__in'] = ids

    return conditions


def process_tags(request: HttpRequest, conditions: dict):
    """Build a conditions with included tags"""
    ids = set()
    for tag in Tag.objects.all():
        status = request.GET.get(tag.tag)
        if status == 'on':
            for q in tag.quizzes.all():
                ids.add(q.id)

    if ids:
        existing = conditions.get('id__in')
        if existing:  # ids that were filtered before should not be overriden
            ids.intersection_update(existing)
            print(ids)

        conditions['id__in'] = ids

    return conditions


def get_completion(request: HttpRequest):
    """Get Completion by token"""
    token = request.POST.get('csrfmiddlewaretoken')
    completion = Completion.objects.get(token=token)

    return completion


def sort_alphabetically_key(quiz: Quiz):
    """Key for sorting quizzes alphabetically"""
    return settings.ALPHABET.find(str(quiz.name)[0].lower())


def convert_tags_to_table(tags):
    rows = []
    row = []
    for i, t in enumerate(tags):
        row.append(t)
        if (i + 1) % 4 == 0:
            rows.append(row.copy())
            row.clear()

    return rows

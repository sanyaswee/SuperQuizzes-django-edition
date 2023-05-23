from django.contrib.auth import get_user
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from .models import Quiz, Question, Completion, UserAnswer


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

        return render(request, 'home/form.html', {'quiz_name': quiz.name, 'quiz_id': quiz.id, 'questions': questions})
    else:
        return redirect('index')


def result(request: HttpRequest):
    if request.method == 'POST':
        post_copy = dict(request.POST)
        post_copy.pop('csrfmiddlewaretoken')

        quiz = Quiz.objects.get(id=post_copy.pop('quiz-id')[0])
        completed_as = post_copy.pop('completed-as')[0]
        is_form = False

        if completed_as == 'form':
            is_form = True

        completion = Completion(
            quiz=quiz, is_form=is_form, start_time=post_copy.pop('start-time')[0]
        )
        user = get_user(request)
        if not user.is_anonymous:
            completion.user = user
        completion.save()

        right_answers = 0
        total_questions = 0
        answers = []
        for q, a in post_copy.items():
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

        score = round(right_answers / total_questions * 100, 2)
        completion.score = score
        completion.save()

        completion = Completion.objects.get(id=completion.id)

        time_taken = completion.end_time - completion.start_time

        return render(
            request, 'home/result.html',
            {
                'right_answers': right_answers,
                'total_questions': total_questions,
                'score': score,
                'answers': answers,
                'time_taken': time_taken.seconds,
            }
        )
    else:
        return redirect('index')


def filter_view(request: HttpRequest):
    if request.method == 'GET':
        conditions = {'available': True}

        search = request.GET.get('search')
        if search:
            conditions['searchable__contains'] = search.lower()

        quizzes = Quiz.objects.filter(**conditions)
        if len(quizzes) == 0:
            return render(request, 'home/nothing_found.html')

        color_classes = ['red-box', 'yellow-box', 'blue-box', 'green-box']
        return render(request, 'home/quiz_list.html', {'quizzes': quizzes, 'color_classes': color_classes})

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from .models import Quiz, Question


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

        right_answers = 0
        total_questions = 0
        answers = []
        for q, a in post_copy.items():
            db_object = Question.objects.get(question=q)
            answer = [q, a[0], db_object.right_answer]

            if a[0] == db_object.right_answer:
                right_answers += 1
                answer.append('Так')
            else:
                answer.append('Ні')

            total_questions += 1
            answers.append(answer)

        score = round(right_answers / total_questions * 100, 2)

        return render(
            request, 'home/result.html',
            {'right_answers': right_answers, 'total_questions': total_questions, 'score': score, 'answers': answers}
        )
    else:
        return redirect('index')

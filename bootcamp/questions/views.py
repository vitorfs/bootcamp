from django.shortcuts import render, redirect
from django.http import HttpResponse
from bootcamp.questions.models import Question, Answer
from bootcamp.questions.forms import QuestionForm, AnswerForm
from bootcamp.activities.models import Activity
from django.db.models import Q

def questions(request):
    questions = Question.objects.all()
    return render(request, 'questions/questions.html', {'questions': questions, 'active': 'all'})

def answered(request):
    questions = Question.get_answered()
    return render(request, 'questions/questions.html', {'questions': questions, 'active': 'answered'})

def unanswered(request):
    questions = Question.get_unanswered()
    return render(request, 'questions/questions.html', {'questions': questions, 'active': 'unanswered'})

def ask(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
           question = Question()
           question.user = request.user
           question.title = form.cleaned_data.get('title')
           question.description = form.cleaned_data.get('description')
           question.tags = form.cleaned_data.get('tags')
           question.save()
           return redirect('/questions/')
        else:
            return render(request, 'questions/ask.html', {'form': form})        
    else:
        form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})

def question(request, pk):
    question = Question.objects.get(pk=pk)
    form = AnswerForm(initial={'question': question})
    return render(request, 'questions/question.html', {'question': question, 'form': form})

def answer(request):
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.user = request.user
            answer.question = form.cleaned_data.get('question')
            answer.description = form.cleaned_data.get('description')
            answer.save()
            return redirect(u'/questions/{0}/'.format(answer.question.pk))
        else:
            question = form.cleaned_data.get('question')
            return render(request, 'questions/question.html', {'question': question, 'form': form})
    else:
        return redirect('/questions/')

def accept(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    answer.accept()
    return HttpResponse('')

def vote(request):
    answer_id = request.POST['answer']
    answer = Answer.objects.get(pk=answer_id)
    vote = request.POST['vote']
    user = request.user
    activity = Activity.objects.filter(Q(activity_type=Activity.UP_VOTE) | Q(activity_type=Activity.DOWN_VOTE), user=user, answer=answer_id)
    if activity:
        activity.delete()
    if vote in [Activity.UP_VOTE, Activity.DOWN_VOTE]:
        activity = Activity(activity_type=vote, user=user, answer=answer_id)
        activity.save()
    return HttpResponse(answer.calculate_votes())

def favorite(request):
    question_id = request.POST['question']
    question = Question.objects.get(pk=question_id)
    user = request.user
    activity = Activity.objects.filter(activity_type=Activity.FAVORITE, user=user, question=question_id)
    if activity:
        activity.delete()
    else:
        activity = Activity(activity_type=Activity.FAVORITE, user=user, question=question_id)
        activity.save()
    return HttpResponse(question.calculate_favorites())

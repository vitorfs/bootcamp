from django.shortcuts import render, redirect
from bootcamp.questions.models import Question
from bootcamp.questions.forms import QuestionForm

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
    return render(request, 'questions/question.html', {'question': question})
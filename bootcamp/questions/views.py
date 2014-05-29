from django.shortcuts import render
from bootcamp.questions.models import Question
from bootcamp.questions.forms import QuestionForm

def questions(request):
    questions = Question.objects.all()
    return render(request, 'questions/questions.html', {'questions': questions})

def ask(request):
    form = QuestionForm()
    return render(request, 'questions/ask.html', {'form': form})
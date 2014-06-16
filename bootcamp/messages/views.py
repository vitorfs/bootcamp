from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required
from django.contrib.auth.models import User

@login_required
def inbox(request):
    return render(request, 'messages/inbox.html')

@login_required
def new(request):
    users = User.objects.filter(is_active=True)
    return render(request, 'messages/new.html', {'users': users})

@login_required
def conversation(request, username):
    return render(request, 'messages/conversation.html')

@login_required
@ajax_required
def delete(request):
    return HttpResponse()

@login_required
@ajax_required
def send(request):
    return HttpResponse()
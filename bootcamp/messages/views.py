from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from bootcamp.decorators import ajax_required

@login_required
def inbox(request):
    return render(request, 'messages/inbox.html')

@login_required
def sent(request):
    return render(request, 'messages/sent.html')

@login_required
def compose(request):
    return render(request, 'messages/compose.html')

@login_required
@ajax_required
def delete(request):
    return HttpResponse()

@login_required
def reply(request):
    return HttpResponse()

@login_required
def message(request, id):
    return render(request, 'messages/message.html')
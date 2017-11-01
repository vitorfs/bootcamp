from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from bootcamp.decorators import ajax_required
from bootcamp.messenger.models import Message


@login_required
def inbox(request):
    conversations = Message.get_conversations(user=request.user)
    users_list = User.objects.filter(
        is_active=True).exclude(username=request.user).order_by('username')
    active_conversation = None
    messages = None
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        messages = Message.objects.filter(user=request.user,
                                          conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0

    return render(request, 'messenger/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'users_list': users_list,
        'active': active_conversation
        })


@login_required
def messages(request, username):
    conversations = Message.get_conversations(user=request.user)
    users_list = User.objects.filter(
        is_active=True).exclude(username=request.user).order_by('username')
    active_conversation = username
    messages = Message.objects.filter(user=request.user,
                                      conversation__username=username)
    messages.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0

    return render(request, 'messenger/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'users_list': users_list,
        'active': active_conversation
        })


@login_required
@ajax_required
def delete(request):
    return HttpResponse()


@login_required
@ajax_required
def send(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return HttpResponse()

        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message)
            return render(request, 'messenger/includes/partial_message.html',
                          {'message': msg})

        return HttpResponse()

    else:
        return HttpResponseBadRequest()


@login_required
@ajax_required
def check(request):
    count = Message.objects.filter(user=request.user, is_read=False).count()
    return HttpResponse(count)

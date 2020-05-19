import os
from PIL import Image
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView
from django.conf import settings
from .models import User
from ..helpers import ajax_required
from bootcamp.notifications.models import Notification, create_notification_handler
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from ..news.models import News


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    paginate_by = 20
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['user_activity'] = News.objects.filter(user=context['user'])
        return context


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):
    fields = [
        "name",
        "email",
        "job_title",
        "location",
        "bio",
        "personal_url",
    ]
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


@login_required
def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:  # pragma: no cover
        pass

    return render(request, 'users/user_picture.html',
                  {'uploaded_picture': uploaded_picture})


@login_required
def upload_picture(request):
    try:
        profile_pictures = settings.MEDIA_ROOT + '/profile_pics/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)

        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/picture/?upload_picture=uploaded')

    except Exception:
        return redirect('/picture/')


@login_required
def save_uploaded_picture(request):
    try:
        x = int(request.POST.get('x'))
        y = int(request.POST.get('y'))
        w = int(request.POST.get('w'))
        h = int(request.POST.get('h'))
        tmp_filename = settings.MEDIA_ROOT + '/profile_pics/' + \
                       request.user.username + '_tmp.jpg'
        filename = settings.MEDIA_ROOT + '/profile_pics/' + \
                   request.user.username + '.jpg'
        im = Image.open(tmp_filename)
        cropped_im = im.crop((x, y, w + x, h + y))
        cropped_im.thumbnail((200, 200), Image.ANTIALIAS)
        cropped_im.save(filename)
        os.remove(tmp_filename)

    except Exception:
        pass

    return redirect('/picture/')


class FollowersPageView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the followers list per user.
    """
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    paginate_by = 20
    template_name = 'users/user_followers.html'
    context_object_name = 'users'

    def get_queryset(self, **kwargs):
        return self.request.user.followers.all()


class FollowingPageView(LoginRequiredMixin, DetailView):
    """
    Basic ListView implementation to call the following list per user.
    """
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    paginate_by = 20
    template_name = 'users/user_following.html'
    context_object_name = 'users'

    def get_queryset(self, **kwargs):

        return self.request.user.following.all()


@login_required
@ajax_required
def follow_user(request, user_id):
    """
    Ajax call to follow a user.
    """
    user = get_object_or_404(User,
                             id=user_id)
    if request.user in user.followers.all():
        user.followers.remove(request.user)
        text = 'Follow'
    else:
        user.followers.add(request.user)
        create_notification_handler(request.user, user, Notification.FOLLOW, key="social_update")
        text = 'Unfollow'
    return HttpResponse(text)


@login_required
@ajax_required
def send_message_request(request, user_id):
    """
    Ajax call to send a message request.
    """
    receiver = get_object_or_404(User, id=user_id)
    contacter = request.user

    if contacter in receiver.pending_list.all():
        receiver.pending_list.remove(contacter)
        text = 'Send Request'
    else:
        receiver.pending_list.add(contacter)
        create_notification_handler(contacter, receiver, Notification.FRIEND_REQUEST, key="social_update")
        text = 'Request Sent'
    return HttpResponse(text)


@login_required
@ajax_required
def accept_message_request(request, user_id):
    """
    Ajax call to accept a message request.
    """
    sender = get_object_or_404(User, id=user_id)
    acceptor = request.user

    if sender in acceptor.pending_list.all():
        acceptor.pending_list.remove(sender)
        acceptor.contact_list.add(sender)
        sender.contact_list.add(acceptor)
        create_notification_handler(acceptor, sender, Notification.FRIEND_ACCEPT, key="social_update")

        text = 'Added to contact list'
    else:
        text = 'Unexpected error!'
    return HttpResponse(text)


@login_required
def block_spammer(request, user_id):
    """
    Remove user from requester's contact list.
    """
    spammer = get_object_or_404(User, id=user_id)
    blocker = request.user

    if spammer in blocker.contact_list.all():
        blocker.contact_list.remove(spammer)
        spammer.contact_list.remove(blocker)
        return redirect('users:detail', username=spammer)
    else:
        return redirect('/')


@login_required
def all_message_requests(request, username):
    """
    Displays a message requests list of users.
    """
    user = User.objects.get(username=username)
    message_requests = user.pending_list.all()

    paginator = Paginator(message_requests, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        users = paginator.page(page)

    except PageNotAnInteger:
        users = paginator.page(1)

    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    p_obj = users

    return render(request, 'users/user_friend_requests.html', {
        'user': user,
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })


@login_required
def all_friends(request, username):
    """
    Displays a friends list of users.
    """
    user = User.objects.get(username=username)
    user_contact_list = user.contact_list.all()

    paginator = Paginator(user_contact_list, 20)
    page = request.GET.get('page')
    if paginator.num_pages > 1:
        p = True
    else:
        p = False
    try:
        users = paginator.page(page)

    except PageNotAnInteger:
        users = paginator.page(1)

    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    p_obj = users

    return render(request, 'users/user_friends.html', {
        'user': user,
        'users': users,
        'page': page,
        'p': p,
        'p_obj': p_obj
    })
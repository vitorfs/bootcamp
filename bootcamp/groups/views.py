from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

import requests
from PIL import Image

from .decorators import user_is_not_banned_from_group, user_is_group_admin
from .forms import GroupForm
from .models import Group
from ..helpers import ajax_required
from ..news.models import News
from ..utils import check_image_extension


class GroupsPageView(ListView):
    """
    Basic ListView implementation to call the groups list.
    """
    model = Group
    queryset = Group.objects.all()
    paginate_by = 20
    template_name = 'groups/view_all_groups.html'
    context_object_name = 'groups'


class GroupPageView(ListView):
    """
    Basic ListView implementation to call the news list per group.
    """
    model = News
    paginate_by = 20
    template_name = 'groups/group.html'
    context_object_name = 'news'

    def get_queryset(self, **kwargs):
        self.group = get_object_or_404(Group,
                                       slug=self.kwargs['group'])
        return self.group.submitted_news.all()
        # return self.group.submitted_news.filter(active=True)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["bv"] = True
        context["admins"] = self.group.admins.all()
        context["group"] = self.group
        return context


class UserSubscriptionListView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the subscriptions list per user.
    """
    model = Group
    paginate_by = 10
    template_name = 'groups/user_subscription_list.html'
    context_object_name = 'subscriptions'

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User,
                                 username=self.request.user)
        return user.subscribed_groups.all()


@login_required
@ajax_required
@user_is_not_banned_from_group
def subscribe(request, group):
    """
    Subscribes a group & returns subscribers count.
    """
    group = get_object_or_404(Group,
                              slug=group)
    user = request.user
    if group in user.subscribed_groups.all():
        group.subscribers.remove(user)
    else:
        group.subscribers.add(user)
    return HttpResponse(group.subscribers.count())


class UserCreatedGroupsPageView(LoginRequiredMixin, ListView):
    """
    Basic ListView implementation to call the groups list per user.
    """
    model = Group
    paginate_by = 20
    template_name = 'groups/user_created_groups.html'
    context_object_name = 'user_groups'

    def get_queryset(self, **kwargs):
        user = get_object_or_404(User,
                                 username=self.request.user)
        return user.inspected_groups.all()


@login_required
def new_group(request):
    """
    Displays a form & handle action for creating new group.
    """
    group_form = GroupForm()

    if request.method == 'POST':
        group_form = GroupForm(request.POST, request.FILES)
        if group_form.is_valid():
            new_group = group_form.save()
            new_group.admins.add(request.user)
            new_group.subscribers.add(request.user)
            return redirect(new_group.get_absolute_url())
            
    form_filling = True

    return render(request, 'groups/new_group.html', {
        'group_form': group_form, 'form_filling': form_filling
    })


@login_required
@user_is_group_admin
def edit_group_cover(request, group):
    """
    Displays edit form for group cover and handles edit action.
    """
    group = get_object_or_404(Group,
                              slug=group)
    if request.method == 'POST':
        group_cover = request.FILES.get('cover')
        if check_image_extension(group_cover.name):
            group.cover = group_cover
            group.save()
            return redirect('group', group=group.slug)
        else:
            return HttpResponse('Filetype not supported. Supported filetypes are .jpg, .png etc.')
    else:
        form_filling = True
        return render(request, 'groups/edit_group_cover.html', {
            'group': group, 'form_filling': form_filling
        })


@login_required
@user_is_group_admin
def banned_users(request, group):
    """
    Displays a list of banned users to the group admins.
    """
    group = get_object_or_404(Group,
                              slug=group)
    users = group.banned_users.all()

    paginator = Paginator(users, 20)
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
    bv = True

    return render(request, 'groups/banned_users.html', {
        'group': group,
        'bv': bv,
        'page': page,
        'p_obj': p_obj,
        'p': p,
        'users': users
    })


@login_required
@user_is_group_admin
def ban_user(request, group, user_id):
    """
    Handles requests from group admins to ban users from the group.
    """
    group = get_object_or_404(Group,
                              slug=group)
    user = get_object_or_404(User,
                             id=user_id)
    if group in user.subscribed_groups.all():
        group.subscribers.remove(user)
        group.banned_users.add(user)
        return redirect('banned_users', group=group.slug)
    else:
        group.banned_users.remove(user)
        return redirect('banned_users', group=group.slug)

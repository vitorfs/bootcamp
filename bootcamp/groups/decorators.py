from django.core.exceptions import PermissionDenied

from .models import Group


def user_is_group_admin(f):
    def wrap(request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs['group'])
        if request.user in group.admins.all():
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def user_is_not_banned_from_group(f):
    def wrap(request, *args, **kwargs):
        group = Group.objects.get(slug=kwargs['group'])
        if not request.user in group.banned_users.all():
            return f(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap

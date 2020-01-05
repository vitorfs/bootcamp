from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def paginate_data(qs, page_size, page, paginated_type, **kwargs):
    """Helper function to turn many querysets into paginated results at
    dispose of our GraphQL API endpoint."""
    p = Paginator(qs, page_size)
    try:
        page_obj = p.page(page)

    except PageNotAnInteger:
        page_obj = p.page(1)

    except EmptyPage:
        page_obj = p.page(p.num_pages)

    return paginated_type(
        page=page_obj.number,
        pages=p.num_pages,
        has_next=page_obj.has_next(),
        has_prev=page_obj.has_previous(),
        objects=page_obj.object_list,
        **kwargs
    )


def ajax_required(f):
    """Not a mixin, but a nice decorator to validate than a request is AJAX"""

    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()

        return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


class AuthorRequiredMixin(View):
    """Mixin to validate than the loggedin user is the creator of the object
    to be edited or updated."""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user != self.request.user:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)


def is_owner(obj, username):
    """
    Checks if model instance belongs to a user
    Args:
        obj: A model instance
        username(str): User's username
    Returns:
        boolean: True is model instance belongs to user else False
    """
    if obj.user.username == username:
        return True
    return False


def update_votes(obj, user, value):
    """
    Updates votes for either a question or answer
    Args:
        obj: Question or Answer model instance
        user: User model instance voting an anwser or question
        value(str): 'U' for an up vote or 'D' for down vote
    """
    obj.votes.update_or_create(
        user=user, defaults={"value": value},
    )
    obj.count_votes()

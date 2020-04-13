import re
from urllib.parse import urljoin

from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseBadRequest
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

import bs4
import requests


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


def fetch_metadata(text):
    """Method to consolidate workflow to recover the metadata of a page of the first URL found a in
    a given text block.
    :requieres:

    :param text: Block of text of any lenght
    """
    urls = get_urls(text)
    try:
        return get_metadata(urls[0])

    except IndexError:
        return None


def get_urls(text):
    """Method to look for all URLs in a given text, extract them and return them as a tuple of urls.
        :requires:

        :param text: A valid block of text of any lenght.

        :returns:
        A tuple of valid URLs extracted from the text.
        """
    regex = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    return re.findall(regex, text)


def get_metadata(url):
    """This function looks for the page of a given URL, extracts the page content and parses the content
    with bs4. searching for the page meta tags giving priority to the Open Graph Protocol
    https://ogp.me/, then it returns the metadata in case there is any, or tries to build one.
    :requires:

    :param url: Any valid URL to search for.

    :returns:
    A dictionary with metadata from a given webpage.
    """
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.content)
    ogs = soup.html.head.find_all(property=re.compile(r"^og"))
    data = {og.get("property")[3:]: og.get("content") for og in ogs}
    if not data.get("url"):
        data["url"] = url

    if not data.get("title"):
        data["title"] = soup.html.title.text

    if not data.get("image"):
        images = soup.find_all("img")
        if len(images) > 0:
            data["image"] = urljoin(url, images[0].get("src"))

    if not data.get("description"):
        data["description"] = ""
        for text in soup.body.find_all(string=True):
            if (
                text.parent.name != "script"
                and text.parent.name != "style"
                and not isinstance(text, bs4.Comment)
            ):
                data["description"] += text

    data["description"] = re.sub("\n|\r|\t", " ", data["description"])
    data["description"] = re.sub(" +", " ", data["description"])
    data["description"] = data["description"].strip()[:255]

    return data

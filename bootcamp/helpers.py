import re
from urllib.parse import urljoin, urlparse

from django.core.exceptions import PermissionDenied
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseBadRequest, JsonResponse
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
        **kwargs,
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
    regex = (
        regex
    ) = r"(?i)\b((?:https?:(?:\/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:\'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b\/?(?!@)))"
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
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = f"http://{parsed_url.path}"

    try:
        response = requests.get(url, timeout=0.9)
        response.raise_for_status()

    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {"message": _(f"We detected the url {url} but it appears to be invalid.")}
        )

    except requests.exceptions.Timeout as e:
        return JsonResponse(
            _(
                f"We found an error trying to connect to the site {url}, please find more info here:{e}"
            )
        )

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

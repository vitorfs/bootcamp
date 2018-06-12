from django.db.utils import IntegrityError
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseBadRequest, JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, DetailView

from bootcamp.helpers import ajax_required
from bootcamp.qa.models import Question, Answer, Vote
from bootcamp.qa.forms import QuestionForm


class QuestionListView(LoginRequiredMixin, ListView):
    """CBV to render the index view
    """
    model = Question
    paginate_by = 20
    context_object_name = "questions"


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """View to call a given Question object and to render all the details about
    that Question."""
    model = Question
    context_object_name = 'question'


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    View to handle the creation of a new question
    """
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = _('Your question has been created.')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("qa:index")


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """
    View to create new answers for a given question
    """
    model = Answer
    fields = ["content", ]
    message = _("Thank you! Your answer has been posted.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs['question_id']
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse(
            "qa:question_detail", kwargs={"pk": self.kwargs["question_id"]})


@login_required
@ajax_required
def question_vote(request):
    """Function view to receive AJAX call, returns the count of votes a given
    question has recieved."""
    if request.method == "POST":
        question_id = request.POST["question"]
        value = None
        if request.POST["value"] == "U":
            value = True

        else:
            value = False

        question = Question.objects.get(pk=question_id)
        try:
            question.votes.update_or_create(
                user=request.user, defaults={"value": value}, )
            question.count_votes()
            return JsonResponse({"votes": question.total_votes})

        except IntegrityError:
            return JsonResponse({'status': 'false',
                                 'message': _("Database integrity error.")},
                                status=500)

    else:
        return HttpResponseBadRequest(content=_("Wrong request type."))

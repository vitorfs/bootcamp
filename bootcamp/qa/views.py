from django.db.utils import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_http_methods
from django.views.generic import CreateView, ListView, DetailView

from bootcamp.helpers import ajax_required
from bootcamp.qa.models import Question, Answer
from bootcamp.qa.forms import QuestionForm


class QuestionsIndexListView(LoginRequiredMixin, ListView):
    """CBV to render a list view with all the registered questions."""
    model = Question
    paginate_by = 20
    context_object_name = "questions"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["popular_tags"] = Question.objects.get_counted_tags()
        context["active"] = "all"
        return context


class QuestionAnsListView(QuestionsIndexListView):
    """CBV to render a list view with all question which have been already
    marked as answered."""
    def get_queryset(self, **kwargs):
        return Question.objects.get_answered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "answered"
        return context


class QuestionListView(QuestionsIndexListView):
    """CBV to render a list view with all question which haven't been marked
    as answered."""
    def get_queryset(self, **kwargs):
        return Question.objects.get_unanswered()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["active"] = "unanswered"
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """View to call a given Question object and to render all the details about
    that Question."""
    model = Question
    context_object_name = "question"


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    View to handle the creation of a new question
    """
    form_class = QuestionForm
    template_name = "qa/question_form.html"
    message = _("Your question has been created.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse("qa:index_noans")


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """
    View to create new answers for a given question
    """
    model = Answer
    fields = ["content", ]
    message = _("Thank you! Your answer has been posted.")

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question_id = self.kwargs["question_id"]
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse(
            "qa:question_detail", kwargs={"pk": self.kwargs["question_id"]})


@login_required
@ajax_required
@require_http_methods(["POST"])
def question_vote(request):
    """Function view to receive AJAX call, returns the count of votes a given
    question has recieved."""
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

    except IntegrityError:  # pragma: no cover
        return JsonResponse({'status': 'false',
                             'message': _("Database integrity error.")},
                            status=500)


@login_required
@ajax_required
@require_http_methods(["POST"])
def answer_vote(request):
    """Function view to receive AJAX call, returns the count of votes a given
    answer has recieved."""
    answer_id = request.POST["answer"]
    value = None
    if request.POST["value"] == "U":
        value = True

    else:
        value = False

    answer = Answer.objects.get(uuid_id=answer_id)
    try:
        answer.votes.update_or_create(
            user=request.user, defaults={"value": value}, )
        answer.count_votes()
        return JsonResponse({"votes": answer.total_votes})

    except IntegrityError:  # pragma: no cover
        return JsonResponse({'status': 'false',
                             'message': _("Database integrity error.")},
                            status=500)


@login_required
@ajax_required
@require_http_methods(["POST"])
def accept_answer(request):
    """Function view to receive AJAX call, marks as accepted a given answer for
    an also provided question."""
    answer_id = request.POST["answer"]
    answer = Answer.objects.get(uuid_id=answer_id)
    answer.accept_answer()
    return JsonResponse({'status': 'true'}, status=200)

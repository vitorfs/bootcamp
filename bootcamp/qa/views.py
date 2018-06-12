from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.views.generic import CreateView, ListView, DetailView

from bootcamp.qa.models import Question, Answer
from bootcamp.qa.forms import QuestionForm, AnswerForm


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
    fields = ["question", "content"]
    message = _("Thank you! Your answer has been posted.")

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)

        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            form.instance.user = self.request.user
            data = {
                "question": self.object.question,
                "content": self.object.content
            }
            return JsonResponse(data)

        else:
            return response


    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse(
            "qa:detail", kwargs={"id": self.kwargs["question_id"]})

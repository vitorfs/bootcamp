from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
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


class AnswerListView(LoginRequiredMixin, ListView):
    model = Answer
    paginate_by = 5
    context_object_name = "answers"


class QuestionDetailView(LoginRequiredMixin, DetailView):
    """View to call a given Question object and to render all the details about
    that Question."""
    model = Question
    context_object_name = 'question'


class AnswerDetailView(LoginRequiredMixin, DetailView):
    """View to call a given Answer object and to render all the details about
    that Answer."""
    model = Answer
    context_object_name = 'answer'


class CreateQuestionView(LoginRequiredMixin, CreateView):
    """
    View to handle the creation of a new question
    """
    model = Question
    fields = ["title", "content", "tags", "status"]
    message = _('Your question has been created.')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse('qa_index')


class CreateAnswerView(LoginRequiredMixin, CreateView):
    """
    View to create new answers for a given question
    """
    model = Answer
    fields = ["question", "description"]
    message = _('Thank you! Your answer has been posted.')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, self.message)
        return reverse(
            'question_detail', kwargs={'uuid_id': self.kwargs['question_id']})

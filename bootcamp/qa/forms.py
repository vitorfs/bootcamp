from django import forms

from bootcamp.qa.models import Answer, Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]


class AnswerForm(forms.ModelForm):
    question = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                      queryset=Question.objects.all())
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4'}),
        max_length=2000)

    class Meta:
        model = Answer
        fields = ["question", "description"]

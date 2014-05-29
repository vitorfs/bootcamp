from django import forms
from bootcamp.questions.models import Question

class QuestionForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), 
        max_length=2000)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        required=False,
        help_text='Use spaces to separate the tags, such as "asp.net mvc5 javascript"')

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
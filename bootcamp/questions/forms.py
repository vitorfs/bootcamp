from django import forms
from bootcamp.questions.models import Question

class QuestionForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=255)
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), 
        max_length=2000)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        help_text="Use commas to separe the tags.")

    class Meta:
        model = Question
        fields = ['title', 'description', 'tags']
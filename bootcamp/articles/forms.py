from django import forms
from bootcamp.articles.models import Article

class ArticleForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), 
        max_length=255)
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}), 
        max_length=4000)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),
        max_length=255,
        required=False,
        help_text='Use spaces to separate the tags, such as "java jsf primefaces"')

    class Meta:
        model = Article
        fields = ['title', 'content', 'tags', 'status']
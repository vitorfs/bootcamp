from django import forms

from .models import Group


class GroupForm(forms.ModelForm):
    """
    Form that handles group data.
    """
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}))
    cover = forms.ImageField(
        widget=forms.FileInput(),
        help_text="Image dimensions should be <b>900 &#10005; 300</b>.",
        required=False
    )

    class Meta:
        model = Group
        fields = ('title', 'description', 'cover')

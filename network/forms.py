from .models import Posts
from django import forms

class PostForm(forms.ModelForm):
    model = Posts
    fields = ["post_title", "post"]
    widgets = {
            "post_title": forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the title'}),
            "post": forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your post here...', 'rows': 5}),
            }
from django.db import models
from django import forms
from .models import Post,Gallery
from django import forms
from django.forms import ClearableFileInput
class ModelPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'body',
            'tags',
            'status',
        ]

class Filles(forms.ModelForm):
    class Meta:
        model = Gallery
        fields = ['title','file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }
from django.db import models
from django import forms
from .models import Post,Gallery
from django import forms
class ModelPost:
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'tags',
        ]

class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')
    class Meta:
        model = Gallery
        fields = ('image', )
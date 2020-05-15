from django.db import models
from .models import Post
from django import forms
class ModelPost:
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
            'tags',
        ]


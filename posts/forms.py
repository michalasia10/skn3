from django.db import models
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

class GalleryForm:
    class Meta:
        model = Gallery
        fields = [
            'name',
            'gallery_img',
        ]
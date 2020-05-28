from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse


# Create your models here.
class PublishManager(models.Manager):
    def get_queryset(self):
        return super(PublishManager, self).get_queryset().filter(status='published')


class ProjectManager(models.Manager):
    def get_queryset(self):
        return super(ProjectManager, self).get_queryset().filter(status='projects')


class AboutManager(models.Manager):
    def get_queryset(self):
        return super(AboutManager, self).get_queryset().filter(status='about')


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'), ('projects', 'Projects'), ('about', 'About'))
    title = models.CharField(max_length=250, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    objects = models.Manager()
    published = PublishManager()
    projects = ProjectManager()
    about = AboutManager()
    created = models.DateTimeField(auto_now=True)
    tags = TaggableManager(blank=True)
    slug = models.SlugField(unique_for_date='publish', max_length=250)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[
            self.publish.year,
            self.publish.strftime('%m'),
            self.publish.strftime('%d'),
            self.slug])

class Gallery(models.Model):
    title = models.CharField(max_length=256,null=True)
    file = models.FileField(upload_to="files/%Y/%m/%d")
    publish = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(unique_for_date='publish', max_length=250)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:gallery_detail', args=[
            self.publish.year,
            self.publish.strftime('%m'),
            self.publish.strftime('%d'),
            self.slug])



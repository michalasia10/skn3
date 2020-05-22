from django.contrib import admin
from django.urls import path
from . import views
# from .views import SearchView

app_name = 'posts'
urlpatterns = [
    path('',views.post_list, name = 'post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>',views.post_detail,name='post_detail'),
    path('tag/<slug:tag_slug>/',views.post_list, name = 'post_list_by_tag'),
    path('search/',views.post_search , name = 'post_search'),
    path('projects/',views.project_list , name = 'projects_list'),
    path('about/',views.about_list , name = 'about'),
    path('contact/',views.contact, name = 'contact'),
    path('add_photo/',views.add_gallery, name = 'add_photo'),
]
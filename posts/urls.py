from django.contrib import admin
from django.urls import path
from . import views
from .views import UpdatePost
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
    path('new/',views.new_post, name='new'),
    # path('edit_post/<int:year>/<int:month>/<int:day>/<slug:post>',views.edit_post ,name = 'edit_post')
    path('edit_post/<int:year>/<int:month>/<int:day>/<slug:post>', UpdatePost.as_view(),name = 'edit_post')
    # path('add_photo/',views.add_gallery, name = 'add_photo'),
    # path('gallery/',views.gallery_list,name = 'gallery'),
    # path('gallery/<int:year>/<int:month>/<int:day>/<slug:image>/',views.gallery_detail,name='gallery_detail'),
]
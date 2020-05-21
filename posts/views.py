from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .models import Post
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity,SearchVector,SearchQuery,SearchRank
from django.views.generic import ListView
from django.db.models import Q
# from .forms import SerachForm
"""POST LIST ZWRACA GRUPĘ/LISTE POSTÓW"""
def post_list(request,tag_slug = None):
    object = Post.published.all()
    paginator = Paginator(object,3)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object = object.filter(tags__in=[tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    #     Jeśli zmienna page nie jest liczba całkowitą pobierana jest pierwsza strona wyników
        posts = paginator.page(1)
    except EmptyPage:
    #     Jeśli zmienna page ma wartość wieksza niz numer ostatniej strony wwtedy pobierana jest ostatnia strone
        posts = paginator.page(paginator.num_pages)
    return render(request,'posts/post_list.html',{'page':page,
                                                'posts':posts,
                                                  'tag':tag,})
                                                  # 'search_tearm':search_term})
"""POST DETAIL ZWRACA JEDNEGO POSTA"""
def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post,slug = post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day,)
    post_tags_id = post.tags.values_list('id',flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id = post.id)
    similar_posts = similar_posts.annotate(same_tags =Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,'posts/post_detail.html',{'post': post,
                                                    'similar_posts':similar_posts})

""" UŻYJ POST_DETAIL DLA STRONA GŁÓWNA W CELU WYŚWIETLENIA POSTA NAJNOWSZEGO DODAJ SOBIE FILTR"""
def post_home(request):
    posts = Post.published.all()
    return render(request,'posts/actual.html',{'posts': posts})

"""Wyszukiwanie postów"""
def post_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query)

            results = Post.objects.annotate(similarity=TrigramSimilarity('title',query)).filter(similarity__gt=0.025).order_by('-similarity')

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'posts/search.html', context)

        else:
            return render(request, 'posts/search.html')

    else:
        return render(request, 'posts/search.html')


def project_list(request,tag_slug = None):
    object = Post.projects.all()
    paginator = Paginator(object,3)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        object = object.filter(tags__in=[tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    #     Jeśli zmienna page nie jest liczba całkowitą pobierana jest pierwsza strona wyników
        posts = paginator.page(1)
    except EmptyPage:
    #     Jeśli zmienna page ma wartość wieksza niz numer ostatniej strony wwtedy pobierana jest ostatnia strone
        posts = paginator.page(paginator.num_pages)
    return render(request,'posts/projects_lists.html',{'page':page,
                                                'posts':posts,
                                                  'tag':tag,})


def about_list(request,tag_slug = None):
    posts = Post.about.order_by('-publish')[:1]
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag,slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request,'posts/about.html',{'posts':posts,
                                                'tag':tag,})
def contact(request):
    return render(request, 'posts/contact.html')
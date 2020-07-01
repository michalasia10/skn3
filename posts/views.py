from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post
from taggit.models import Tag
from django.db.models import Count
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import Q
from .forms import  ModelPost
from django.contrib import messages


"""POST LIST ZWRACA GRUPĘ/LISTE POSTÓW"""


def post_list(request, tag_slug=None):
    object = Post.published.all()
    paginator = Paginator(object, 3)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object = object.filter(tags__in=[tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #     Jeśli zmienna page nie jest liczba całkowitą pobierana jest pierwsza strona wyników
        posts = paginator.page(1)
    except EmptyPage:
        #     Jeśli zmienna page ma wartość wieksza niz numer ostatniej strony wwtedy pobierana jest ostatnia strone
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/post_list.html', {'page': page,
                                                    'posts': posts,
                                                    'tag': tag, })
    # 'search_tearm':search_term})


"""POST DETAIL ZWRACA JEDNEGO POSTA"""


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'posts/post_detail.html', {'post': post,
                                                      'similar_posts': similar_posts})


""" UŻYJ POST_DETAIL DLA STRONA GŁÓWNA W CELU WYŚWIETLENIA POSTA NAJNOWSZEGO DODAJ SOBIE FILTR"""


def post_home(request):
    posts = Post.published.all()
    return render(request, 'posts/actual.html', {'posts': posts})


# edytuj post
def edit_post(request, year, month, day, post):
    submit = False
    template = 'posts/edit.html'
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )
    if request == 'POST':
        form = ModelPost(request.POST or None, instance=post)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Post został uaktualniony')
                return HttpResponseRedirect('/posts/edit_post?submit=True')
        except Exception as e:
            messages.warning(request, 'Post nie został dodany przez błąd: {}'.format(e))

    else:
        form = ModelPost(instance=post)
        if 'submit' in request.GET:
            submit = True

    context = {'form': form,
               'post': post,
               'submit':submit}
    return render(request, template, context)

def delete(request, year, month, day, post):
    template = 'posts/new_post.html'
    post = get_object_or_404(Post, slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day, )
    if request == 'POST':
        form = ModelPost(request.POST or None, instance=post)

        try:
            if form.is_valid():
                form.save()
                messages.success(request, 'Post został uaktualniony')
        except Exception as e:
            messages.warning(request, 'Post nie został dodany przez błąd: {}'.format(e))

    else:
        form = ModelPost(instance=post)

    context = {'form': form,
               'post': post}
    return render(request, template, context)
# def updatebc(request, pk):
#     instance = get_object_or_404(BaseCase, pk=pk)
#     instance.base_case_name
#     bcform = BaseCaseForm(request.POST or None,instance=instance)
#     if bcform.is_valid():
#         instance = bcform.save(commit=False)
#         instance.save()
#     context = {
#         'bcform':bcform,
#         'instance': instance,
#     }
#     return render(request, 'update.html', context)
"""Wyszukiwanie postów"""


def post_search(request):
    if request.method == 'GET':
        query = request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            lookups = Q(title__icontains=query) | Q(content__icontains=query)

            results = Post.objects.annotate(similarity=TrigramSimilarity('title', query)).filter(
                similarity__gt=0.025).order_by('-similarity')
            # results = Post.objects.annotate(rank=TrigramSimilarity('title',query)).filter(rank__gte=0.025).order_by('rank')

            context = {'results': results,
                       'submitbutton': submitbutton}

            return render(request, 'posts/search.html', context)

        else:
            return render(request, 'posts/search.html')

    else:
        return render(request, 'posts/search.html')


def project_list(request, tag_slug=None):
    object = Post.projects.all()
    paginator = Paginator(object, 3)
    page = request.GET.get('page')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object = object.filter(tags__in=[tag])
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        #     Jeśli zmienna page nie jest liczba całkowitą pobierana jest pierwsza strona wyników
        posts = paginator.page(1)
    except EmptyPage:
        #     Jeśli zmienna page ma wartość wieksza niz numer ostatniej strony wwtedy pobierana jest ostatnia strone
        posts = paginator.page(paginator.num_pages)
    return render(request, 'posts/projects_lists.html', {'page': page,
                                                         'posts': posts,
                                                         'tag': tag, })


def about_list(request, tag_slug=None):
    posts = Post.about.order_by('-publish')[:1]
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    return render(request, 'posts/about.html', {'posts': posts,
                                                'tag': tag, })


def contact(request):
    return render(request, 'posts/contact.html')


# Nowy post zmien nazwe zmien
def new_post(request):
    submitted = False
    if request.method == 'POST':
        form = ModelPost(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            form.save()
            # assert False
            return HttpResponseRedirect('/posts/new?submitted=True')
    else:
        form = ModelPost()
        if 'submitted' in request.GET:
            submitted = True

    return render(request,
                  'posts/new_post.html',
                  {'form': form, 'submitted': submitted}
                  )

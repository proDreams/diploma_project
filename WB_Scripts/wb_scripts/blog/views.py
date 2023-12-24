import json
from itertools import chain
from json import JSONDecodeError

from django import http
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .forms import NewsForm, NewsForPostsForm, PostsForNewsForm, ScriptsForm, FeedbackForm
from .models import Post, Category, RecentlyPosts, create_recently_viewed_record, increase_post_view_count, News, \
    increase_news_view_count, NewsForPosts, ScriptsForPosts, ExtendedUser
from .utils import slugify


class ChangeColorTheme:

    def __init__(self):
        self.color = None
        self.user = None

    def get_user_theme(self, request):
        try:
            self.user = ExtendedUser.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            self.user = ExtendedUser.objects.create(user_id=request.user.id, color_scheme='dark')
        return self.user.color_scheme

    def change_user_theme(self, request):
        try:
            self.color = json.loads(request.body.decode())['color']
            ExtendedUser.objects.filter(user_id=request.user.id).update(color_scheme=self.color)
        except JSONDecodeError:
            pass


def feedback(request):
    feedback_form = FeedbackForm(request.POST, user=request.user)
    if feedback_form.is_valid():
        feedback_form = feedback_form.save(commit=False)
        feedback_form.save()
        return 'Отправлено'
    else:
        return FeedbackForm(user=request.user)


@login_required
def search(request):
    search_post = request.GET.get('search')
    if search_post:
        posts = Post.objects.filter(Q(title__icontains=search_post) | Q(description__icontains=search_post))
        scripts = ScriptsForPosts.scr_man.filter(Q(title__icontains=search_post) | Q(script__icontains=search_post))
        news = News.news_man.filter(Q(title__icontains=search_post) | Q(body__icontains=search_post))
    else:
        posts = []
        scripts = []
        news = []

    result_list = list(chain(posts, scripts, news))

    paginator = Paginator(result_list, 8)
    page_number = request.GET.get('page', 1)
    results = paginator.page(page_number)

    feedback_form = feedback(request)
    if feedback_form == 'Отправлено':
        return http.HttpResponseRedirect(request.path)

    cs = ChangeColorTheme()
    if request.method == 'POST':
        cs.change_user_theme(request)
    color_scheme = cs.get_user_theme(request)

    context = {
        'results': results,
        'search_post': search_post,
        'feedback_form': feedback_form,
        'color_scheme': color_scheme,
    }

    return render(request,
                  'blog/search_result.html',
                  context)


@login_required
def index(request):
    category_list = Category.cat_man.get_queryset()
    recently_upd_posts_list = Post.post_man.all()
    recently_viewed_posts_list = RecentlyPosts.rec_man.get_recently_posts(request.user.id)
    most_viewed_posts = Post.post_man.get_most_visited()

    feedback_form = feedback(request)
    if feedback_form == 'Отправлено':
        return http.HttpResponseRedirect(request.path)

    cs = ChangeColorTheme()
    if request.method == 'POST':
        cs.change_user_theme(request)
    color_scheme = cs.get_user_theme(request)

    context = {
        'recently_upd_posts_list': recently_upd_posts_list,
        'category_list': category_list,
        'recently_viewed_posts_list': recently_viewed_posts_list,
        'most_viewed_posts': most_viewed_posts,
        'feedback_form': feedback_form,
        'color_scheme': color_scheme,
    }

    return render(request,
                  'blog/index.html',
                  context)


@login_required
def post_detail(request, id_: int, slug):
    create_recently_viewed_record(request.user.id, id_)
    increase_post_view_count(id_)
    related_news_for_post = NewsForPosts.nfp_man.get_related_news(id_)
    related_scripts_for_post = ScriptsForPosts.scr_man.get_related_scripts(id_)
    post = get_object_or_404(Post,
                             id=id_,
                             status=Post.Status.PUBLISHED)
    paginator = Paginator(related_news_for_post, 3)
    page_number = request.GET.get('page', 1)
    related_news_list = paginator.page(page_number)

    form = PostsForNewsForm(request.POST, post_id=id_)
    if form.is_valid() and not NewsForPosts.nfp_man.check_exists(id_, form.data['news']):
        form.save()
        return http.HttpResponseRedirect(request.path)
    else:
        form = PostsForNewsForm(post_id=id_)

    form2 = ScriptsForm(request.POST, user=request.user, post=id_)
    if form2.is_valid():
        form2 = form2.save(commit=False)
        form2.save()
        return http.HttpResponseRedirect(request.path)
    else:
        form2 = ScriptsForm(user=request.user, post=id_)

    feedback_form = feedback(request)
    if feedback_form == 'Отправлено':
        return http.HttpResponseRedirect(request.path)

    cs = ChangeColorTheme()
    if request.method == 'POST':
        cs.change_user_theme(request)
    color_scheme = cs.get_user_theme(request)

    context = {
        "post": post,
        'related_news_list': related_news_list,
        'related_scripts_for_post': related_scripts_for_post,
        'form': form,
        'form2': form2,
        'feedback_form': feedback_form,
        'color_scheme': color_scheme,
    }

    return render(request,
                  'blog/post_page.html',
                  context)


@login_required
def category_page(request, id_, slug):
    sub_category_list = Category.cat_man.get_queryset(parent=id_)
    category_posts_list = Post.post_man.get_sub_category_posts(id_)
    paginator = Paginator(category_posts_list, 6)
    page_number = request.GET.get('page', 1)
    posts_list = paginator.page(page_number)

    feedback_form = feedback(request)
    if feedback_form == 'Отправлено':
        return http.HttpResponseRedirect(request.path)

    cs = ChangeColorTheme()
    if request.method == 'POST':
        cs.change_user_theme(request)
    color_scheme = cs.get_user_theme(request)

    context = {
        "sub_category_list": sub_category_list,
        "title": Category.objects.get(id=id_),
        "posts_list": posts_list,
        'feedback_form': feedback_form,
        'color_scheme': color_scheme,
    }

    return render(request, 'blog/category_page.html', context)


@login_required
def news_detail(request, id_, slug):
    increase_news_view_count(id_)
    related_post_list = NewsForPosts.nfp_man.get_related_posts(id_)
    news = get_object_or_404(News,
                             id=id_)

    form = NewsForPostsForm(request.POST, news_id=id_)
    if form.is_valid() and not NewsForPosts.nfp_man.check_exists(form.data['post'], id_):
        form.save()
        return http.HttpResponseRedirect(request.path)
    else:
        form = NewsForPostsForm(news_id=id_)

    feedback_form = feedback(request)
    if feedback_form == 'Отправлено':
        return http.HttpResponseRedirect(request.path)

    cs = ChangeColorTheme()
    if request.method == 'POST':
        cs.change_user_theme(request)
    color_scheme = cs.get_user_theme(request)

    context = {
        "news": news,
        "related_post_list": related_post_list,
        'form': form,
        'feedback_form': feedback_form,
        'color_scheme': color_scheme,
    }

    return render(request,
                  'blog/news_page.html',
                  context)


@login_required
def news_list_page(request):
    news_list_all = News.news_man.all().order_by('-publish')
    paginator = Paginator(news_list_all, 6)
    page_number = request.GET.get('page', 1)
    news_list = paginator.page(page_number)

    form = NewsForm(request.POST, user=request.user)
    if form.is_valid():
        form = form.save(commit=False)
        form.slug = slugify(form.title)
        form.save()
        return http.HttpResponseRedirect(request.path)
    else:
        form = NewsForm(user=request.user)

    feedback_form = feedback(request)
    if feedback_form == 'Отправлено':
        return http.HttpResponseRedirect(request.path)

    cs = ChangeColorTheme()
    if request.method == 'POST':
        cs.change_user_theme(request)
    color_scheme = cs.get_user_theme(request)

    context = {
        "news_list": news_list,
        'form': form,
        'feedback_form': feedback_form,
        'color_scheme': color_scheme,
    }

    return render(request, 'blog/news_list_page.html', context)

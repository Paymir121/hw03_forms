from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.conf import settings

from .forms import PostForm
from .models import Group, Post, User


def page(request,posts):
    paginator = Paginator(posts, settings.PAGINATION_SIZE)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    posts = Post.objects.select_related('group', "author")
    template = 'posts/index.html'
    context = {
        'page_obj': page(request, posts),
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.select_related("group", "author")
    template = 'posts/group_list.html'
    context = {
        'group': group,
        'page_obj': page(request, posts),
    }
    return render(request, template, context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_count = Post.objects.select_related('group', "author").count
    posts = Post.objects.select_related('group', "author")
    template = 'posts/profile.html'
    context = {
        'author': author,
        'post_count': post_count,
        'page_obj': page(request, posts),
    }
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author_post = Post.objects.filter(author=post.author).count()
    template = 'posts/post_detail.html'
    context = {
        'post': post,
        'author_post': author_post,
        'user_can_edit': request.user == post.author,
    }
    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/post_create.html'
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts:profile", request.user)
    form = PostForm()
    context = {
        'form': form,
    }
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    template = 'posts/post_create.html'
    post = Post.objects.get(pk=post_id)
    if request.user != post.author:
        return redirect("posts:post_detail", post.pk)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post.pk)
    context = {'form': form, 'is_edit': True, 'post': post}
    return render(request, template, context)

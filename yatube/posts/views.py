from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User
from .utils import paginator

POST_SHOW_LMT = 10


def index(request):
    post_list = Post.objects.select_related('group')
    page_obj = paginator(request, post_list, POST_SHOW_LMT)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = paginator(request, post_list, POST_SHOW_LMT)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = author.posts.all()
    page_obj = paginator(request, post_list, POST_SHOW_LMT)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    context = {
        'post': post,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            author = request.user
            post = Post(text=text, author=author, group=group)
            post.save()
            return redirect('posts:profile', username=request.user.username)
        return render(request, 'posts/create_post.html', {'form': form})
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post_id and request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/create_post.html', {'form': form})
    form.fields['text'].help_text = 'Текст нового поста'
    return render(request,
                  'posts/create_post.html',
                  {
                      'form': form,
                      'is_edit': True,
                      'post': post
                  }
                  )

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from .forms import PostForm
from .models import Post, Group, User

POST_SHOW_LMT = 10


def index(request):
    post_list = Post.objects.select_related('group')
    paginator = Paginator(post_list, POST_SHOW_LMT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    paginator = Paginator(post_list, POST_SHOW_LMT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    written_posts = author.posts.count()
    post_list = author.posts.all()
    paginator = Paginator(post_list, POST_SHOW_LMT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'author': author,
        'written_posts': written_posts,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    written_posts = post.author.posts.count()
    context = {
        'post': post,
        'written_posts': written_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
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
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']
            post.text = text
            post.group = group
            post.save()
            return redirect('posts:post_detail', post_id=post_id)
        return render(request, 'posts/create_post.html', {'form': form})

    form = PostForm(
        initial={
            'text': post.text,
            'group': post.group.pk if post.group else 0
        }
    )
    form.fields['text'].help_text = 'Текст нового поста'
    return render(request,
                  'posts/create_post.html',
                  {
                      'form': form,
                      'is_edit': True,
                      'post': post
                  }
                  )

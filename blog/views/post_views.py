from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from blog.models import Post, Category
from blog.forms import PostForm
from django.contrib import messages
from django.db.models import Q

# Create your views here


def list(request):

    search = request.GET.get('search', '')
    if search:
        post_list = Post.objects.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        ).order_by('-created_at')
    else:
        post_list = Post.objects.all().order_by('-created_at')

    paginator = Paginator(post_list, 2)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    return render(request, 'blog/list.html', {'posts': posts})


def details(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'blog/details.html', {'post': post})


def create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post created successfully')
            return redirect('list')
    return render(request, 'blog/create.html', {'form': form})


def edit(request, id):
    categories = Category.objects.all()
    post = get_object_or_404(Post, id=id)
    form = PostForm(instance=post)

    if request.method == 'POST':
        old_name = post.thumb.name if post.thumb else None
        old_storage = post.thumb.storage if post.thumb else None
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            if 'thumb' in request.FILES and old_name:
                old_storage.delete(old_name)
            form.save()
            return redirect('blog_details', id=post.id)

    return render(request, 'blog/edit.html', {'form': form, 'post': post, 'categories':categories})


def delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        if post.thumb:
            post.thumb.delete(save=False)
        post.delete()
        messages.warning(request, 'Post deleted successfully')
        return redirect('list')
    return render(request, 'blog/confirm_delete.html', {'post': post})


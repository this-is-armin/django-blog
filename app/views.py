from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Category, Post, Comment


class HomeView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(request, self.template_name)


class BlogView(View):
    template_name = 'blog.html'

    def get(self, request):
        posts = Post.objects.filter(is_published=True)

        if request.GET.get('search'):
            posts = posts.filter(title__contains=request.GET['search'])

        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, self.template_name, {
            'posts': posts,
            'page_obj': page_obj,
        })


class DetailView(View):
    template_name = 'detail.html'

    def setup(self, request, *args, **kwargs):
        self.post_instance = get_object_or_404(Post, slug=kwargs['slug'], is_published=True)
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not self.post_instance.is_published:
            return redirect('app:blog')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        post = self.post_instance
        comments = post.comments.filter(is_published=True)
        return render(request, self.template_name, {
            'post': post,
            'comments': comments,
        })
    
    def post(self, request, **kwargs):
        post = self.post_instance
        user = request.POST.get('user')
        body = request.POST.get('body')

        invalid_chars = ['(', ')', '[', ']', '{', '}', '<', '>', '/', '\\', '|', ',', '.', '~', '`', '!', '?', '@', '#', '$', '%', '^', '&', '*', '_', '-', '+', '=']
        invalid_names = ['admin', 'ADMIN']
        
        for char in invalid_chars:
            if char in user:
                messages.error(request, 'Your name was contain incorrect character(s)')
                return redirect(post.get_absolute_url)

        for name in invalid_names:
            if user == name:
                messages.error(request, f"Your name can't be '{name}'")
                return redirect(post.get_absolute_url)
            
            if name in user:
                messages.error(request, f"Your name can't contain '{name}'")
                return redirect(post.get_absolute_url)

        Comment.objects.create(post=post, user=user, body=body)
        messages.success(request, 'Your comment was sent successfully')
        
        return redirect(post.get_absolute_url)


class CategoryView(View):
    template_name = 'category.html'

    def get(self, request, **kwargs):
        category = get_object_or_404(Category, slug=kwargs['slug'])
        posts = category.posts.filter(is_published=True)

        if request.GET.get('search'):
            posts = posts.filter(title__contains=request.GET['search'])

        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        return render(request, self.template_name, {
            'category': category,
            'posts': posts,
            'page_obj': page_obj,
        })
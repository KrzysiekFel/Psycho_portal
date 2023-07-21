from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import BlogPosts
from django.http import HttpRequest, HttpResponse
from typing import List, Type


def about(request: HttpRequest) -> HttpResponse:
    return render(request, 'about.html', {'title': 'About'})


class BlogPostsListView(ListView):
    model: Type[BlogPosts] = BlogPosts
    template_name: str = 'blog/home.html'
    context_object_name: str = 'posts'
    ordering: List[str] = ['-date_posted']
    paginate_by: int = 3


class PostDetailedView(DetailView):
    model: Type[BlogPosts] = BlogPosts
    template_name: str = 'blog/post.html'

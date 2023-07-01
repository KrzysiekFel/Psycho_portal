from django.shortcuts import render
from django.views.generic.list import ListView
from .models import BlogPosts


def about(request):
    return render(request, 'about.html', {'title': 'About'})


class BlogPostsListView(ListView):
    model = BlogPosts
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4


from django.urls import path
from .views import about, BlogPostsListView, PostDetailedView

urlpatterns = [
    path('', BlogPostsListView.as_view(), name='blog-posts'),
    path('about/', about, name='about'),
    path('post/<int:pk>', PostDetailedView.as_view(), name='post-detail'),
]

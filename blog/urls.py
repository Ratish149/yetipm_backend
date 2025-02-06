from django.urls import path
from .views import (
    PostListCreateView, PostDetailView, PostListSlugView, RecentPostsView,
    AuthorListCreateView, AuthorDetailView, CategoryListCreateView, CategoryDetailView,
    TagListCreateView, TagDetailView
)

urlpatterns = [
    path('blogs/', PostListCreateView.as_view(), name='post_list'),
    path('latest-blogs/', RecentPostsView.as_view(), name='recent_posts'),
    path('blogs-slug/', PostListSlugView.as_view(), name='post_list_slug'),
    path('blogs-single/<str:slug>/', PostDetailView.as_view(), name='post_single'),
    path('authors/', AuthorListCreateView.as_view(), name='author-list-create'),
    path('authors/<int:id>/', AuthorDetailView.as_view(), name='author-detail'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<str:category_name>/', CategoryDetailView.as_view(), name='category-detail'),
    path('tags/', TagListCreateView.as_view(), name='tag-list-create'),
    path('tags/<int:id>/', TagDetailView.as_view(), name='tag-detail'),
]

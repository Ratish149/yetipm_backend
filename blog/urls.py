from django.urls import path
from .views import post_list,post_single,post_list_slug,recent_posts,similar_listings

urlpatterns = [
    path('posts/', post_list, name='post_list'),
    path('latest-posts/', recent_posts, name='recent_posts'),
    path('posts-slug/', post_list_slug, name='post_list_slug'),
    path('post-single/<str:slug>/', post_single, name='post_single'),
    path('posts/similar/<slug:slug>/', similar_listings, name='similar_listings'),
]
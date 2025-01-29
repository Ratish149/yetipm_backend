from django.urls import path
from .views import post_list,post_single,post_list_slug,recent_posts

urlpatterns = [
    path('blogs/', post_list, name='post_list'),
    path('latest-blogs/', recent_posts, name='recent_posts'),
    path('blogs-slug/', post_list_slug, name='post_list_slug'),
    path('blogs-single/<str:slug>/', post_single, name='post_single'),
]
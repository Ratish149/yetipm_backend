from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Post,Tag,Category
from .serializers import PostSerializer,PostSmallSerializer,TagSerializer,CategorySerializer,TagSmallSerializer,CategorySmallSerializer,PostSlugSerializer
from bs4 import BeautifulSoup


@api_view(['GET'])
def post_list(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        tags = Tag.objects.all()
        categories = Category.objects.all()
        serializer = PostSmallSerializer(posts, many=True)
        tag_serializer = TagSerializer(tags, many=True)
        categories_serializer = CategorySerializer(categories, many=True)
        return Response({
            "posts":serializer.data,
            "tags":tag_serializer.data,
            "categories":categories_serializer.data,
        })

@api_view(['GET'])
def post_list_slug(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSlugSerializer(posts, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def post_single(request, slug):
    if request.method == 'GET':
        posts = Post.objects.get(slug=slug)
        html_string = posts.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(toc_div)
        serializer = PostSerializer(posts)

        # New code to get similar listings
        similar_posts = Post.objects.filter(
            tags__in=posts.tags.all()
        ).exclude(slug=slug)[:5]
        similar_serializer = PostSmallSerializer(similar_posts, many=True)

        return Response({
            "data": serializer.data,
            "toc": updated_html_string,
            "similar_listings": similar_serializer.data,  # Include similar listings
        })
    
@api_view(['GET'])
def recent_posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()[:5]
        posts_serializer = PostSerializer(posts,many=True)
        return Response({
          "recent_posts":posts_serializer.data,
        })



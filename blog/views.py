from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Tag, Category, Author
from .serializers import (
    PostSerializer, PostSmallSerializer, TagSerializer, CategorySerializer,
    TagSmallSerializer, CategorySmallSerializer, PostSlugSerializer, AuthorSerializer
)
from bs4 import BeautifulSoup

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostSmallSerializer
        return PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        posts_serializer = self.get_serializer(queryset, many=True)
        tags_serializer = TagSerializer(Tag.objects.all(), many=True)
        categories_serializer = CategorySerializer(Category.objects.all(), many=True)
        
        return Response({
            "posts": posts_serializer.data,
            "tags": tags_serializer.data,
            "categories": categories_serializer.data,
        })

class PostListSlugView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSlugSerializer

class PostDetailView(generics.RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSmallSerializer
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        post = self.get_object()
        html_string = post.blog_content
        soup = BeautifulSoup(html_string, 'html.parser')
        toc_div = soup.find('div', class_='mce-toc')
        if toc_div is not None:
            toc_div.extract()
        updated_html_string = str(toc_div)
        
        similar_posts = Post.objects.filter(tags__in=post.tags.all()).exclude(slug=post.slug).distinct()[:5]
        similar_serializer = PostSmallSerializer(similar_posts, many=True)
        
        return Response({
            "data": self.get_serializer(post).data,
            "toc": updated_html_string,
            "similar_listings": similar_serializer.data,
        })

class RecentPostsView(generics.ListAPIView):
    queryset = Post.objects.order_by('-created_at')[:5]
    serializer_class = PostSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({"recent_posts": serializer.data})

class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    lookup_field = 'id'

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'id'

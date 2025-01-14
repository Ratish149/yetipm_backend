from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics,filters
from .models import Blog
from .serializers import BlogSerializer
# Create your views here.

class BlogList(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    lookup_field = 'slug'


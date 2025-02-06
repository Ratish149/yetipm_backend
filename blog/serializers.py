from rest_framework import serializers
from .models import Author, Category, Tag, Post
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from bs4 import BeautifulSoup

class HTMLField(serializers.CharField):
    def to_representation(self, value):
        return str(BeautifulSoup(value, 'html.parser'))

    def to_internal_value(self, data):
        return data

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        depth = 2

class CategorySmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('category_name',)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        depth = 2

class TagSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('tag_name',)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
        depth = 2


class PostSerializer(serializers.ModelSerializer):
    category=serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author=serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())
    tags=serializers.PrimaryKeyRelatedField(many=True, queryset=Tag.objects.all())
    class Meta:
        model = Post
        fields = '__all__'
        depth = 2
        ordering = ['-created_at']
    
    # def get_blog_content(self, obj):
    #     html_string = obj.blog_content
    #     soup = BeautifulSoup(html_string, 'html.parser')
    #     toc_div = soup.find('div', class_='mce-toc')
    #     if toc_div is not None:
    #         toc_div.extract()
    #     updated_html_string = str(soup)
    #     return mark_safe(updated_html_string)

class PostSmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        depth = 1
        ordering = ['-created_at']


class PostSlugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('slug',)
        depth = 1
from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import Blog
from unfold.admin import ModelAdmin
# Register your models here.

class BlogAdmin(ModelAdmin): 
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(Blog, BlogAdmin)

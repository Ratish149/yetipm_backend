from django.contrib import admin
from .models import Author,Category,Post,Tag
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django.db import models

admin.site.register(Author, ModelAdmin)
admin.site.register(Category, ModelAdmin)
admin.site.register(Tag, ModelAdmin)


class PostAdmin(ModelAdmin):
   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'blog_content':
            kwargs['widget'] = TinyMCE()
        return super().formfield_for_dbfield(db_field, **kwargs)
   
admin.site.register(Post,PostAdmin)

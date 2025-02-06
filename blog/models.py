from django.db import models

from tinymce import models as tinymce_models
from django.utils.text import slugify


class SlugMixin:
    def generate_unique_slug(self):
        base_slug = slugify(self.title)
        slug = base_slug

        model = self.__class__
        while model.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = base_slug

        self.slug = slug

    def save(self, *args, **kwargs):
        self.generate_unique_slug()
        super().save(*args, **kwargs)


class Author(models.Model):
    name = models.CharField(max_length=200) 
    role = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    picture = models.FileField(null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=200,primary_key=True)
    category_image = models.FileField(blank=True, null=True)

    def __str__(self):
        return self.category_name

class Tag(models.Model):
    tag_name = models.CharField(max_length=200)

    def __str__(self):
        return self.tag_name


class Post(SlugMixin,models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=300, unique=True,null=True,blank=True)
    title = models.CharField(max_length=500)
    blog_duration_to_read = models.CharField(max_length=100,blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    thumbnail_image = models.FileField(null=True, blank=True)
    thumbnail_image_alt_description = models.CharField(max_length=300,null=True,blank=True)
    blog_content = tinymce_models.HTMLField(blank=True)
    tags = models.ManyToManyField(Tag,blank=True)
    author = models.ForeignKey(Author, on_delete=models.DO_NOTHING)
    meta_title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=500,blank=True)
    meta_keywords = models.CharField(max_length=200,blank=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


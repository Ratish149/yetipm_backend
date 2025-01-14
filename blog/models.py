from django.db import models
# Create your models here.
from django.utils.text import slugify
class SlugMixin:
    def generate_unique_slug(self):
        if not self.title:  # Skip if title is not set
            return
            
        base_slug = slugify(self.title)
        slug = base_slug
        model = self.__class__
        # Check if the slug already exists
        if model.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = base_slug  # Just use the base slug if it exists
        self.slug = slug

class Tag(models.Model):
    name = models.CharField(max_length=220)

    def __str__(self):
        return self.name

class Blog(SlugMixin, models.Model):
    title = models.CharField(max_length=220)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/',null=True,blank=True)
    slug = models.SlugField(unique=True, blank=True,max_length=220)
    tags = models.ManyToManyField(Tag, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.generate_unique_slug()  # Ensure slug is updated when saving
        super().save(*args, **kwargs)  # Call the original save method
    


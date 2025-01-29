from django.db import models
from django.utils.text import slugify

class SlugMixin:
    def generate_unique_slug(self):
        if not self.name:  # Skip if name is not set
            return
            
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        model = self.__class__
        while model.objects.filter(slug=slug).exclude(id=self.id).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        self.slug = slug

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not set
            self.generate_unique_slug()
        super().save(*args, **kwargs)

class State(SlugMixin, models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=2)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class City(SlugMixin, models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Image(models.Model):
    image = models.FileField(upload_to='images/')

    def __str__(self):
        return str(self.image)

class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class Features(models.Model):
    image = models.FileField(blank=True, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    
class Project(SlugMixin, models.Model):
    PROJECT_TYPE_CHOICES = [
        ('Single Family', 'Single Family'),
        ('Condominium', 'Condominium'),
        ('Townhouse', 'Townhouse'),
        ('Duplex', 'Duplex'),
        ('Other', 'Other'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    project_type = models.CharField(max_length=100, choices=PROJECT_TYPE_CHOICES,default='Single Family')
    project_address = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_breakdown = models.TextField(blank=True)
    project_description = models.TextField(blank=True)
    area_square_footage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    garage_spaces = models.IntegerField(blank=True, null=True)
    images = models.ManyToManyField(Image, blank=True)
    features = models.ManyToManyField(Features, blank=True)
    bedrooms = models.IntegerField()
    bathrooms = models.FloatField()
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    availability = models.BooleanField(default=True)
    avialable_date = models.DateField(blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Inquiry(models.Model):
    INQUIRY_TYPES = [
        ('Specific Property', 'Specific Property'),
        ('General Inquiry', 'General Inquiry'),
    ]

    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES,null=True,blank=True)
    property = models.ForeignKey(Project, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True,)

    def __str__(self):
        return f"{self.inquiry_type} - {self.first_name} {self.last_name}"
    
class Testimonial(models.Model):
    SOURCE_CHOICES = [
        ('Google', 'Google'),
        ('Facebook', 'Facebook'),
        ('Yelp', 'Yelp'),
        ('Zillow', 'Zillow'),
        ('Other', 'Other'),
    ]
    name = models.CharField(max_length=100)
    testimonial = models.TextField()
    image = models.FileField()
    source = models.CharField(max_length=100, choices=SOURCE_CHOICES,default='Other')

    def __str__(self):
        return self.name
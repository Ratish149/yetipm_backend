from django.db import models

# Create your models here.
class OurTeam(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    email= models.EmailField(null=True,blank=True)
    profile_picture = models.FileField(null=True,blank=True)
    profile_picture_alt_description = models.CharField(max_length=200,null=True,blank=True)
    facebook_link = models.URLField(null=True,blank=True)
    instagram_link= models.URLField(null=True,blank=True)
    twitter_link = models.URLField(null=True,blank=True)
    linkedin_link = models.URLField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.name

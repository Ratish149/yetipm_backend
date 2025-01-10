from django.contrib import admin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import (
     State, City, Image,
    FAQ, Project, Testimonial,Inquiry
)

@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']

@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']
    search_fields = ['name']


@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['name', 'project_type']
    list_filter = ['project_type']
    search_fields = ['name', 'project_address']
    filter_horizontal = ['images']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    list_display = ['inquiry_type', 'property', 'name', 'email', 'submitted_at']
    list_filter = ['inquiry_type', 'submitted_at']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['submitted_at']


@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = ['image']

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ['question']
    search_fields = ['question']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ['name', 'source']
    list_filter = ['source']
    search_fields = ['name']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

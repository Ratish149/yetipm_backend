from django.contrib import admin
from unfold.admin import ModelAdmin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import (
    State, City, Image, Features,
    FAQ, Project, Testimonial, Inquiry
)

@admin.register(State)
class StateAdmin(ModelAdmin):
    list_display = ['name', 'abbreviation']
    search_fields = ['name', 'abbreviation']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(City)
class CityAdmin(ModelAdmin):
    list_display = ['name', 'state']
    list_filter = ['state']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Features)
class FeaturesAdmin(ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Project)
class ProjectAdmin(ModelAdmin):
    list_display = ['name', 'project_type', 'price', 'availability']
    list_filter = ['project_type', 'availability', 'city']
    search_fields = ['name', 'project_address']
    filter_horizontal = ['images', 'features']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Inquiry)
class InquiryAdmin(ModelAdmin):
    list_display = ['inquiry_type', 'property', 'first_name', 'last_name', 'email', 'submitted_at']
    list_filter = ['inquiry_type', 'submitted_at']
    search_fields = ['first_name', 'last_name', 'email', 'phone_number']
    readonly_fields = ['submitted_at']

@admin.register(Image)
class ImageAdmin(ModelAdmin):
    list_display = ['image']

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ['question']
    search_fields = ['question', 'answer']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

@admin.register(Testimonial)
class TestimonialAdmin(ModelAdmin):
    list_display = ['name', 'source']
    list_filter = ['source']
    search_fields = ['name', 'testimonial']
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

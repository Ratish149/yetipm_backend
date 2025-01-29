from django.contrib import admin
from .models import OurTeam
from unfold.admin import ModelAdmin
from django.db import models
from tinymce.widgets import TinyMCE

# Register your models here.
class OurTeamAdmin(ModelAdmin):
    list_display = ('name', 'role', 'email', 'created_at')  # Fields to display in the list view
    search_fields = ('name', 'role')  # Fields to search in the admin
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

admin.site.register(OurTeam, OurTeamAdmin)
from django.contrib import admin
from .models import OurTeam
from unfold.admin import ModelAdmin
# Register your models here.
class OurTeamAdmin(ModelAdmin):
    list_display = ('name', 'role', 'email')  # Fields to display in the list view
    search_fields = ('name', 'role')  # Fields to search in the admin

admin.site.register(OurTeam, OurTeamAdmin)
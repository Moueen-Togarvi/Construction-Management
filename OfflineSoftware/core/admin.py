from django.contrib import admin
from .models import Project, Material

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'created_at', 'updated_at')

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'project', 'quantity', 'unit_price', 'total_cost')

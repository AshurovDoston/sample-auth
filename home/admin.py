from django.contrib import admin
from .models import Task

# Register your models here.

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Customize how Task appears in admin panel
    """
    # Columns to display in the task list
    list_display = ['title', 'user', 'completed', 'created_at']

    # Add filters in sidebar
    list_filter = ['completed', 'created_at']

    # Add search functionality
    search_fields = ['title', 'description']

    # Fields that are read-only
    readonly_fields = ['created_at', 'updated_at']

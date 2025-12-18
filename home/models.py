from django.db import models
from django.conf import settings  # To reference the custom User model

# Create your models here.

class Task(models.Model):
    """
    Task model represents a single to-do item.
    Each task belongs to a user and has a title, description, and completion status.
    """

    # Foreign Key: Links each task to a user (many tasks can belong to one user)
    # on_delete=models.CASCADE: If user is deleted, delete their tasks too
    # settings.AUTH_USER_MODEL: References your custom UserProfile model
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tasks'  # Allows user.tasks.all() to get all user's tasks
    )

    # CharField: Short text field (max 200 characters)
    # For the task title/name
    title = models.CharField(max_length=200)

    # TextField: Long text field (unlimited length)
    # optional (blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    # BooleanField: True/False value
    # default=False: New tasks are incomplete by default
    completed = models.BooleanField(default=False)

    # DateTimeField: Stores date and time
    # auto_now_add=True: Automatically set when task is created
    created_at = models.DateTimeField(auto_now_add=True)

    # auto_now=True: Updates every time the task is saved
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Orders tasks by creation date (newest first with '-')
        ordering = ['-created_at']

    def __str__(self):
        # String representation shown in admin panel
        return self.title

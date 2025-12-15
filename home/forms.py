from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    """
    ModelForm: Automatically creates a form based on a Model.

    Why ModelForm?
    - Automatically creates form fields from model fields
    - Handles validation based on model constraints
    - Can save directly to database with form.save()
    - Less code, fewer errors!
    """

    class Meta:
        # Specify which model this form is for
        model = Task

        # Which fields to include in the form
        # We DON'T include 'user', 'created_at', 'updated_at' because:
        # - user: Set automatically from logged-in user
        # - created_at/updated_at: Set automatically by Django
        fields = ['title', 'description', 'completed']

        # Customize field widgets (HTML input types and attributes)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',  # CSS class for styling
                'placeholder': 'Enter task title',
                'maxlength': '200',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Add task description (optional)',
                'rows': 4,
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-checkbox',
            }),
        }

        # Custom labels for form fields
        labels = {
            'title': 'Task Title',
            'description': 'Description',
            'completed': 'Mark as completed',
        }

        # Help text shown below each field
        help_texts = {
            'title': 'What do you need to do?',
            'description': 'Add any additional details here.',
            'completed': 'Check if this task is done.',
        }

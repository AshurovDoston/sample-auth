from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

def home_view(request):
    """
    Home page view - shows all tasks for the logged-in user
    """
    if request.user.is_authenticated:
        # Get all tasks belonging to the current user
        # user.tasks works because of related_name='tasks' in the model
        tasks = request.user.tasks.all()
        # tasks = Task.objects.filter(user=request.user)
        # tasks = Task.objects.all()

    else:
        tasks = None

    context = {
        'tasks': tasks,
    }
    return render(request, "home.html", context)


@login_required  # Decorator: Only logged-in users can access this view
def task_create_view(request):
    """
    View for creating a new task.

    How this works:
    1. GET request (user visits page): Show empty form
    2. POST request (user submits form): Validate and save data
    """

    # Check if this is a POST request (form submission)
    if request.method == 'POST':
        # Create form instance with submitted data
        # request.POST contains all form data from the submission
        form = TaskForm(request.POST)

        # is_valid() checks:
        # - Required fields are filled
        # - Data types are correct (e.g., max_length respected)
        # - Custom validation rules
        if form.is_valid():
            # form.save(commit=False) creates Task object but doesn't save to DB yet
            # We need to set the user before saving
            task = form.save(commit=False)

            # Set the user to the currently logged-in user
            task.user = request.user

            # Now save to database
            task.save()

            # Redirect to home page after successful creation
            # This prevents duplicate submissions if user refreshes
            return redirect('home')

        # If form is NOT valid, it falls through to render the form again
        # Django will automatically display error messages

    else:
        # GET request: Create an empty form
        form = TaskForm()

    # Render the template with the form
    # If POST and invalid: form contains errors
    # If GET: form is empty
    context = {
        'form': form,
    }
    return render(request, 'task_create.html', context)


@login_required
def task_update_view(request, pk):
    # get_object_or_404: Gets the task OR returns 404 if not found
    # This is better than Task.objects.get() which raises an exception
    task = get_object_or_404(Task, pk=pk, user=request.user)
    # Note: We filter by user=request.user for security
    # This ensures users can only edit their own tasks!

    if request.method == 'POST':
        # Create form with submitted data AND the existing task instance
        # instance=task tells Django: "Update this task, don't create a new one"
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            # Since we passed instance=task, save() updates the existing task
            # No need for commit=False since user is already set
            form.save()

            # Redirect to home after successful update
            return redirect('home')

    else:
        # GET request: Create form pre-filled with task's current data
        # instance=task populates the form fields with existing values
        form = TaskForm(instance=task)

    context = {
        'form': form,
        'task': task,  # Pass task to template so we can show "Edit Task: [title]"
    }
    return render(request, 'task_update.html', context)

@login_required
def task_delete_view(request, pk):

    # Get the task, ensuring it belongs to the current user
    task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == 'POST':
        # Delete the task from database
        task.delete()

        # Redirect to home page
        return redirect('home')

    # GET request: Show confirmation page
    context = {
        'task': task,
    }
    return render(request, 'task_delete.html', context)
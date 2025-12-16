from django.urls import path
from .views import home_view, task_create_view, task_update_view, task_delete_view

urlpatterns = [
    # URL pattern: "" (empty string) means the root URL
    # name="home": Used in templates {% url 'home' %}
    path("", home_view, name="home"),

    # URL pattern: "tasks/create/" means /tasks/create/
    # When user visits this URL, Django calls task_create_view()
    # name="task_create": Can reference in templates with {% url 'task_create' %}
    path("tasks/create/", task_create_view, name="task_create"),

    # URL pattern with parameter: <int:pk>
    # <int:pk> captures an integer from URL and passes it as 'pk' argument
    # Example: /tasks/5/edit/ → calls task_update_view(request, pk=5)
    # In template: {% url 'task_update' task.pk %} generates correct URL
    path("tasks/<int:pk>/edit/", task_update_view, name="task_update"),
    path("tasks/<int:pk>/delete/", task_delete_view, name="task_delete"),
]
from django.urls import path
from .views import home_view, task_create_view

urlpatterns = [
    # URL pattern: "" (empty string) means the root URL
    # name="home": Used in templates {% url 'home' %}
    path("", home_view, name="home"),

    # URL pattern: "tasks/create/" means /tasks/create/
    # When user visits this URL, Django calls task_create_view()
    # name="task_create": Can reference in templates with {% url 'task_create' %}
    path("tasks/create/", task_create_view, name="task_create"),
]
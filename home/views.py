from django.shortcuts import render

def home_view(request):
    context = {
        'latest_question_list': 'latest_question_list',
        'my_variable': 'This is a variable from the view'
        }
    return render(request, "home.html", context)
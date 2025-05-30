from django.shortcuts import render

def index(request):
    """
    Render the index page of the application.
    """
    return render(request, 'index.html')
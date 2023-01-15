from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage_view(request, *args, **kwargs):
    my_context = {
        "info": 'Some information'
    }
    return render(request, 'home.html', my_context)


def contact_view(request, *args, **kwargs):
    my_context = {
        "person": "Mirosław Kania",
        "adress": "adress:",
        "number": "mobile:"
    }
    return render(request, 'contact.html', my_context)


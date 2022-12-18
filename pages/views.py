from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage_view(request, *args, **kwargs):
    my_context = {
        "list": [123, 321, 456, 654]
    }
    return render(request, 'home.html', my_context)


def contact_view(request, *args, **kwargs):
    my_context = {
        "abc": "This is my address",
        "adress": "Łąka Dąbrowskiego 5",
        "number": "555-55-55"
    }
    return render(request, 'contact.html', my_context)


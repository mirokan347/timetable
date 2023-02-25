from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def homepage_view(request, *args, **kwargs):
    my_context = {
        "info": 'this is a sample home page that can serve as a business card for the school or display some information'
    }
    return render(request, 'home.html', my_context)


def contact_view(request, *args, **kwargs):
    my_context = {
        "name": "Private School name",
        "adress": "school adress",
        "number": "contact phone number"
    }
    return render(request, 'contact.html', my_context)


def no_permission_view(request, *args, **kwargs):
    my_context = {
        "info": 'Access denied'
    }
    return render(request, 'no_permission.html', my_context)

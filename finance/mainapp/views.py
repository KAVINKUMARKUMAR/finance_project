from django.shortcuts import render,redirect
from django.template import loader
from django.http import HttpResponse,JsonResponse
from .forms import ContactForm
from .models import Contact,Boxes
from django.views.generic import DetailView,UpdateView,DeleteView,ListView,CreateView
# Create your views here.
def homeView(request):
    context = {
    }
    return render(request, 'home.html', context)
def aboutView(request):
    context = {
    }
    return render(request, 'about.html', context)
def servicesView(request):
    context = {
        'Boxes' : Boxes.objects.all()
    }
    return render(request, 'services.html', context)
def calculatorView(request):
    context = {
    }
    return render(request, 'calculator.html', context)
def contactView(request):
    context = {
    }
    return render(request, 'contact.html', context)
def DisclaimerView(request):
    context = {
    }
    return render(request, 'disclaimer.html', context)
def PolicyView(request):
    context = {
    }
    return render(request, 'policy.html', context)
def TermView(request):
    context = {
    }
    return render(request, 'term.html', context)

class Contact(CreateView):
    model = Contact
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = '/'
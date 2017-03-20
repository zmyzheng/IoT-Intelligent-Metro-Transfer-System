from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import  Temperature
from django.template import loader

def index(request):
    
    temperature_list = Temperature.objects.all()
    context = {'temperature_list': enumerate(temperature_list)}
    return render(request, 'polls/index.html', context)

    

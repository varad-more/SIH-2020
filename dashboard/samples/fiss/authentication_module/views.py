from django.shortcuts import render
from django.contrib.auth import authenticate
# Create your views here.

def homepage(request):
    return render(request, 'homepage.html',{})


def detail(request):
    return render (request,'details.html',{})       
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required,permission_required
from dashboard.models import file_download
import mysql.connector 

# Create your views here.

@login_required
def index (request):
    data = file_download.objects.all()[:5]
    content = {
        'data':data
    }

    return render (request , 'index.html',content)

@login_required
def report(request):
    return render (request, 'report.html')
@login_required
def rep_generatoion(request):
    return render (request, 'gen.html') 


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render (request,'register.html', {'form':form})

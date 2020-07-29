from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm 
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required,permission_required

# Create your views here.

@login_required
def index (request):
    return render (request , 'index.html')

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

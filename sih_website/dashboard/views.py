from django.shortcuts import render
 

# Create your views here.
def index (request):
    return render (request , 'index.html')

def report(request):
    return render (request, 'report.html')

def rep_generatoion(request):
    return render (request, 'gen.html') 


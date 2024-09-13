from django.shortcuts import render,redirect
from .forms import *

# Create your views here.
def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        form=Create_user_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form=Create_user_form()
    context={
        'form':form
    }
    return render(request,'register.html',context)

def dashboard(request):
    return render(request,'dashboard.html')
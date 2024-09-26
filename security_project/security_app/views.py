from django.shortcuts import render,redirect
from .forms import *
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        form=Create_user_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('two_factor:login')
    else:
        form=Create_user_form()
    context={
        'form':form
    }
    return render(request,'register.html',context)

@login_required
def dashboard(request):
    return render(request,'dashboard.html')

def user_logout(request):
    auth.logout(request)
    messages.success(request,"Logout success!")
    return redirect('home')

def account_locked(request):
    return render(request,'account-locked.html')
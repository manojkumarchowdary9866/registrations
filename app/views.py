from django.urls import reverse
from cmath import log
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')



def registration(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        ud=UserForm(request.POST)
        pd=ProfileForm(request.POST,request.FILES)
        if ud.is_valid() and pd.is_valid():
            u=ud.save(commit=False)
            u.set_password(ud.cleaned_data.get('password'))
            u.save()
            p=pd.save(commit=False)
            p.user=u
            p.save()
            send_mail('Registration',
                        'Successfull registration',
                        'gade.manojkc@gmail.com',
                        [u.email],fail_silently=False)
            return HttpResponse('registarion is successfull')
    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request,user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def profile(request):
    username=request.session['username']
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)

    return render(request,'profile.html',context={'user':user,'profile':profile})

@login_required
def change_password(request):
    if request.method=='POST':
        username=request.session['username']
        password=request.POST['password']
        user=User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return HttpResponse('password is changed successfully')
    return render(request,'change_password.html')


def forgot_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=User.objects.filter(username=username)
        if user:
            user[0].set_password(password)
            return HttpResponse('reset of password done Successfully')
        else:
            return HttpResponse('please eneter correct user')
    return render(request,'forgot_password.html')
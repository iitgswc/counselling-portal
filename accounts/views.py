from django.contrib.auth import ( authenticate, get_user_model,login,logout,)
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UserLoginForm

def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect("/")
    return render(request,"accounts/form.html", {"form":form, "title":title})

def register_view(request):
    return render(request,"accounts/form.html",{})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
def forgot_password(request):
    return render(request, "accounts/forgot_password.html")


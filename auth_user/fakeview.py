from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import Student

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Student.objects.create(user=user)
            auth_login(request, user)
            messages.success(request, "Account created successfully! Welcome!")
            return redirect("index")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "signup.html", {"form": form})

from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


from .forms import CustomUserCreationForm
from scholarship.models import Student


def index(request):
    if request.user.is_authenticated:
        return render(request, "student/student_home_page.html")
    else:
        return render(request, "index.html")


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
            print(form.errors)  # Log form errors for debugging
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "signup.html", {"form": form})



def login_view(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        index(request)

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # Using the built-in form
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("index")  # TODO: redirect to student view
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()  # Display empty form

    return render(request, "login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")  # Redirect to login after logging out

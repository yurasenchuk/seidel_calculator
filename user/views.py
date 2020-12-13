from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from user.models import CustomUser
from user.forms import RegisterForm, AuthoriseForm


def register(request):
    context = {}
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"{form.cleaned_data.get('first_name')} welcome to our app")
            return redirect("home")
        else:
            context["data"] = form
    else:
        context["data"] = RegisterForm()
    return render(request, "register.html", context=context)


def authorise(request):
    context = {"email": None, "password": None}
    if request.POST:
        form = AuthoriseForm(request.POST)
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = CustomUser.get_by_email(email)
            if user.check_password(password):
                current_user = authenticate(request, email=email, password=password, role=user.role)
                login(request, current_user)
                return redirect("home")
            else:
                context["data"] = form
                messages.warning(request, "Incorrect password")
        except ValueError as ve:
            messages.warning(request, str(ve))
            context["data"] = form
    else:
        form = AuthoriseForm()
        context["data"] = form
    return render(request, "authorise.html", context=context)


def log_out(request):
    logout(request)
    messages.info(request, "Logged out!")
    return redirect("authorise")

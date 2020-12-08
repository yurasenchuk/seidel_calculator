from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from user.models import CustomUser
from user.forms import RegisterForm, AuthoriseForm
from user.checks import check_is_authenticated, check_is_admin


def register(request, id=0):
    context = {}
    if request.POST:
        if id == 0:
            form = RegisterForm(request.POST)
        else:
            user = CustomUser.get_by_id(id)
            form = RegisterForm(request.POST, instance=user)
            context["data"] = form
        if form.is_valid():
            if not id == 0:
                CustomUser.delete_by_id(id)
            user = form.save()
            if id == 0:
                login(request, user)
                messages.success(request, f"{form.cleaned_data.get('first_name')} welcome to our app")
                return redirect("home")
            else:
                messages.success(request, f"User with email: {form.cleaned_data.get('email')} has been updated")
                return redirect("get_users")
        else:
            context["data"] = form
    else:
        if id == 0:
            form = RegisterForm()
        else:
            if not request.user.is_authenticated:
                messages.warning(request, "Log in first!")
                return redirect("authorise")
            if not check_is_admin(request):
                messages.warning(request, "You don`t have permission!")
                return redirect("home")
            user = CustomUser.get_by_id(id)
            form = RegisterForm(instance=user)
        context["data"] = form
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


def get_all(request):
    if not check_is_authenticated(request):
        messages.warning(request, "Log in first!")
        return redirect("authorise")
    if not check_is_admin(request):
        raise PermissionDenied
    users = list(CustomUser.get_all())
    if len(users) == 0:
        raise Http404("You don't have any user registered in system")
    return render(request, "get_users.html", {"users": users})


def delete_user(request, id):
    if not check_is_authenticated(request):
        messages.warning(request, "Log in first!")
        return redirect("authorise")
    if not check_is_admin(request):
        raise PermissionDenied
    if not CustomUser.delete_by_id(id):
        raise Http404("User doesn't exist")
    return redirect("get_users")


def user_info(request, id):
    if not check_is_authenticated(request):
        messages.warning(request, "Log in first!")
        return redirect("authorise")
    if not check_is_admin(request):
        raise PermissionDenied
    if not CustomUser.get_by_id(id):
        raise Http404("User doesn't exist")
    return render(request, "get_user_by_id.html", context={"user": CustomUser.get_by_id(id)})


def block(request, id):
    if not check_is_authenticated(request):
        messages.warning(request, "Log in first!")
        return redirect("authorise")
    if not check_is_admin(request):
        raise PermissionDenied
    if not CustomUser.block(id):
        raise Http404("User doesn't exist")
    return redirect("user_info", id)


def change_role(request, id):
    if not check_is_authenticated(request):
        messages.warning(request, "Log in first!")
        return redirect("authorise")
    if not check_is_admin(request):
        raise PermissionDenied
    if not CustomUser.change_role(id):
        raise Http404("User doesn't exist")
    return redirect("user_info", id)

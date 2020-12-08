from django.contrib import messages
from django.shortcuts import render, redirect
from re import match


def page_not_found(request, exception=None):
    context = {}
    if match(r"[a-zA-z\d]", str(exception)):
        context["exception"] = str(exception)
    else:
        context["exception"] = "Resource not found"
    return render(request, "error.html", status=404, context=context)


def bad_request(request, exception=None):
    return render(request, "error.html", status=400, context={"exception": "Bad request!!!"})


def forbidden(request, exception=None):
    messages.warning(request, "You don`t have permission!")
    return redirect("home")


def unauthorized(request, exception=None):
    messages.warning(request, "Log in first!")
    return redirect("authorise")


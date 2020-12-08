from django.contrib import messages
from django.shortcuts import render, redirect
from user.views import authorise
from calculator.forms import CalculatorForm
from calculator.models import Calculator


def home(request):
    if not request.user.is_authenticated:
        return redirect(authorise)
    context = {}
    if request.POST:
        form = CalculatorForm(request.POST)
        if form.is_valid():
            if "matrix" in form.cleaned_data and "vector" in form.cleaned_data and "e" in form.cleaned_data:
                calculator = Calculator.create(form.cleaned_data["size"], form.cleaned_data["matrix"],
                                               form.cleaned_data["vector"], form.cleaned_data["e"], request.user)
                xi = calculator.calculate_seidel()
                context["xi"] = xi
            else:
                context["form"] = form
        else:
            context["form"] = form
    else:
        if not request.user.is_authenticated:
            messages.warning(request, "Log in first!")
            return redirect("authorise")
        form = CalculatorForm(initial={"size": 0})
        context["form"] = form
    return render(request, "home.html", context=context)

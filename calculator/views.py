from django.contrib import messages
from django.shortcuts import render, redirect
from json import dumps
from user.views import authorise
from calculator.validation import validate_matrix, validate_vector
from calculator.models import Calculator
from calculator.tasks import calculate_seidel_task


def home(request):
    if not request.user.is_authenticated:
        return redirect(authorise)
    context = {}
    if request.POST:
        context["eps"] = float(request.POST.get("eps"))
        context["size"] = int(request.POST.get("size"))
        context["matrix"] = [[0 for j in range(context["size"])] for i in range(context["size"])]
        context["vector"] = [0 for i in range(context["size"])]
        for i in range(context["size"]):
            context["vector"][i] = request.POST.get(f"vector[{i}]")
            for j in range(context["size"]):
                context["matrix"][i][j] = request.POST.get(f"matrix[{i}][{j}]")
        if validate_matrix(context["matrix"]) and validate_vector(context["vector"]):
            if context["eps"] < 0 or context["eps"] >= 1:
                messages.warning(request, "Epsilon should be greater than 0 and less than 1")
            else:
                context["matrix"] = [[float(context["matrix"][j][i]) for i in range(context["size"])] for j in
                                     range(context["size"])]
                context["vector"] = [float(context["vector"][i]) for i in range(context["size"])]
                calculator = Calculator.create(size=context["size"], matrix_a=context["matrix"],
                                               vector_b=context["vector"], e=context["eps"], user=request.user)
                calc = calculate_seidel_task.delay(calculator.id)
                task_id = calc.task_id
                messages.success(request, "Your task has been started")
                context["task_id"] = task_id
                return render(request, "progress.html", context=context)
        else:
            messages.warning(request, "Elements of matrix and vector should be not 0")
    else:
        context["size"] = 0
        context["matrix"] = [[0 for j in range(context["size"])] for i in range(context["size"])]
        context["vector"] = [0 for i in range(context["size"])]
        context["eps"] = 0.001
    context["matrix"] = dumps(context["matrix"])
    context["vector"] = dumps(context["vector"])
    return render(request, "home.html", context=context)


def results_for_user(request):
    if not request.user.is_authenticated:
        return redirect(authorise)
    tasks = Calculator.results(request.user.id)
    tasks.sort(key=lambda x: x.pk, reverse=True)
    tasks = dumps([i.to_dict() for i in tasks])
    return render(request, "results.html", context={"results": tasks})


def clear_tasks(request):
    if not request.user.is_authenticated:
        return redirect(authorise)
    result = Calculator.delete_by_user_id(request.user.id)
    if result:
        messages.success(request, "Successfully cleared")
    else:
        messages.warning(request, "Something went wrong")
    return render(request, "results.html", context={"results": []})


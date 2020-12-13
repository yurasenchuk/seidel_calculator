from django.urls import path
import calculator.views as views

urlpatterns = [
    path('', views.home, name="home"),
    path("tasks", views.results_for_user, name="tasks"),
    path("clear_tasks", views.clear_tasks, name="delete_tasks")
]

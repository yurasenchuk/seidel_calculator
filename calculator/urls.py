from django.urls import path
import calculator.views as views

urlpatterns = [
    path('', views.home, name="home")
]

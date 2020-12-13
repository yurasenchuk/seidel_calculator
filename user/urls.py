from django.urls import path
import user.views as views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("authorise/", views.authorise, name="authorise"),
    path("log_out/", views.log_out, name="log_out"),
]

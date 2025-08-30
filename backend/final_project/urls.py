from django.urls import path

from final_project import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_new_note, name="create"),
    path("login", views.login_view, name="login"),
    path("forgot-password", views.forgot_password_view, name="forgot_password"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
]

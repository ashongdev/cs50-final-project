from django.urls import path

from final_project import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create_new_note, name="create"),
    path("check_user", views.check_user, name="check_user"),
    # path("google_signin", views.sign_in_with_google, name="google_signin"),
]

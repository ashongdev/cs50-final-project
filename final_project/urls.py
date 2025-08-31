from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("all", views.index, name="index"),
    path("archives", views.archives, name="archives"),
    path("deleted", views.deleted, name="deleted"),
    path("create", views.create_new_note, name="create"),
    path("login", views.login_view, name="login"),
    path("forgot-password", views.forgot_password_view, name="forgot_password"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    #
    path("select_note/<str:note_id>", views.select_note, name="select_note"),
    path("archive_note/<str:note_id>", views.archive_note, name="archive_note"),
    path("unarchive_note/<str:note_id>", views.unarchive_note, name="unarchive_note"),
    path("delete_note/<str:note_id>", views.delete_note, name="delete_note"),
    path("restore_note/<str:note_id>", views.restore_note, name="restore_note"),
    path("save_note/<str:note_id>", views.save_note, name="save"),
]

from django.urls import path
from . import views

urlpatterns = [
    path("notes/", views.notes_view, name="notes"),
    path("edit-note/<int:id>/", views.edit_note, name="edit_note"),
    path("delete-note/<int:id>/", views.delete_note, name="delete_note"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
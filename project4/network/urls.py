
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new", views.new, name="new"),
    path("profile/<user>", views.profile, name="profile"),
    path("edit/<id>", views.edit, name="edit"),
    path("follow/<user>", views.follow, name="follow"),
    path("unfollow/<user>", views.unfollow, name="unfollow"),
    path("following", views.following, name="following"),
    path("like/<int:id>/", views.like, name="like")
]

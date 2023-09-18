from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<id>", views.listing, name="view"),
    path("addWatchlist/<id>", views.addWatchlist, name="addWatchlist"),
    path("rmWatchlist/<id>", views.rmWatchlist, name="rmWatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("category/<c>", views.category, name="category"),
    path("categories", views.categories, name="categories"),
    path("bid/<id>", views.bid, name="bid"),
    path("comment/<id>", views.comment, name="comment"),
    path("close/<id>", views.close, name="close")
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:item_id>", views.item_page, name="item_page"),
    path("<int:item_id>/watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_item", views.NewItem, name="new_item"),
    path("mylist", views.mylist, name="mylist")

]

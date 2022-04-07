from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:item_id>", views.item_page, name="item_page"),
    path("<int:item_id>/watchlist", views.watchlist, name="watchlist"),
    path("<int:item_id>/bid", views.bid, name="bid"),
    path("<int:item_id>/endbid", views.endbid, name="endbid"),
    path("<int:item_id>/comment", views.comment, name="comment"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_item", views.NewItem, name="new_item"),
    path("mylist", views.mylist, name="mylist")

]

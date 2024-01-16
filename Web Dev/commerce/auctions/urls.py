from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addtowatchlist/<int:id>", views.add_to_watchlist, name="addwatchlist"),
    path("dellist/<int:id>", views.delete_from_watchlist, name="dellist"),
    path("placebid/<int:id>", views.bid, name="bid"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("create", views.create, name="create"),
    path("auctions", views.auctions, name="auctions"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("close/<int:listing_id>", views.close, name="close"),
    path('comment/<int:listing_id>', views.add_comment, name='comment'),
    path('category/<int:category_id>', views.category, name='category'),
    # path('delete_list/<int:listing_id>/', views.delete_bid, name='delete_listing'),
]

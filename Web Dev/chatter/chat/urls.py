from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('chat/<key>/', views.chat_room_view, name='chat' ),
    path('chatroom', views.chat_rooms_list, name='chatroom'),
    path('friends', views.friends, name='friends'),
    path('friends/<type>/<id>', views.requester, name='friends_operations'),
    path('find/<key>', views.findfriends, name='findfriends'),
    path('changepfp', views.changepfp, name='changepfp')
]
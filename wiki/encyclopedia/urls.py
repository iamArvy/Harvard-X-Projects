from django.urls import path

from . import views

app_name = 'encyclopedia'
urlpatterns = [
    path('', views.index, name="index"),
    path('wiki/<str:q>', views.htmlentry, name="info_path"),
    path('wiki/', views.entry, name="info_search"),
    path('create/', views.create, name='create')
]

from django.urls import path

from . import views

app_name = "network"

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('main/<int:user_id>', views.main, name='main'),
    path('add_fiend/', views.add_friend, name='add_friend'),
    path('add_chat/', views.add_chat, name='add_chat'),
    path('messanger/', views.messanger, name='messanger'),
]

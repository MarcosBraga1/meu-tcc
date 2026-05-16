from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('chat/<int:chat_id>/', views.chat_detail, name='chat_detail'),
    path('chat/<int:chat_id>/rename/', views.rename_chat, name='rename_chat'),
    path('chat/<int:chat_id>/delete/', views.delete_chat, name='delete_chat'),
]
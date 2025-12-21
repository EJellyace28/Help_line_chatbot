from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_view, name='landing'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Chat URLs
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:chat_id>/', views.chat_view, name='chat_detail'),
    
    # Chat API endpoints
    path('api/chat/create/', views.create_chat, name='create_chat'),
    path('api/chat/<int:chat_id>/send/', views.send_message, name='send_message'),
    path('api/chat/<int:chat_id>/delete/', views.delete_chat, name='delete_chat'),
    path('api/chat/<int:chat_id>/rename/', views.rename_chat, name='rename_chat'),
]
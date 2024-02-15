from django.contrib import admin
from django.urls import path
from . import views

app_name = 'user_app'

urlpatterns = [
    path('register/', views.UsuarioCreateView.as_view(), name='registrar'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('update-password/', views.UpdatePasswordView.as_view(), name='update_password'),
    path('verification/<pk>', views.CodeVericationView.as_view(), name='verificacion'),
    
]

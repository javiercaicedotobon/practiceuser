from django.contrib import admin
from django.urls import path
from . import views

app_name = 'home_app'

urlpatterns = [
    path('home/', views.Index.as_view(), name='home'),
    path('mixin/', views.PruebaFecha.as_view(), name='mixin'),
]

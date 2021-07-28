from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home_page, name='home'),
    path(r'pokemon/', views.get_all, name='all-pokemon'),
    path('load_data/', views.load_data, name='update-database'),
]

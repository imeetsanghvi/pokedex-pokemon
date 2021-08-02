from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home_page, name='home'),
    path('pokemon/', views.get_all, name='all-pokemon'),
    # path('developer/', views.get_developer, name='developer'),
    path('load_data/', views.load_data, name='update-database'),
]

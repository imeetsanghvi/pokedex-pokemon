from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home_page, name='home'),
    path('all/', views.get_all, name='all-pokemon'),
    path('region/<region_name>/', views.get_pokemon_from_region, name='pokemon-from-region'),
    path('generation/<gid>/', views.get_pokemon_from_generation, name='pokemon-from-generation'),
    path('types/<type_name>/', views.get_pokemon_from_types, name='pokemon-from-type'),
    path('load_data/', views.load_data, name='update-database'),
]

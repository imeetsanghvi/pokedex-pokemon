from django.contrib import admin
from pokemon.models import Pokemon, Regen, Type
# Register your models here.
admin.site.register(Pokemon)
admin.site.register(Type)
admin.site.register(Regen)
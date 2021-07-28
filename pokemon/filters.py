import django_filters
from pokemon.models import Pokemon, Type

class PokemonFilter(django_filters.FilterSet):    
    class Meta:
        model = Pokemon
        # fields = '__all__'
        fields = ['name',
                  'type_name',
                  'regen'
                  ]
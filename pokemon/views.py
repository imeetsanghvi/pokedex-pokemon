from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.shortcuts import render

from .models import Pokemon, Type

# Create your views here.

types = Type.objects.all()
regions = Pokemon.objects.order_by().values('region').distinct()
generations = Pokemon.objects.order_by().values('generation').distinct()

def get_generation_and_region(id):
    if id in range(1,152):
        return 1, 'Kanto'
    elif id in range(152,252):
        return 2, 'Johto'
    elif id in range(252,387):
        return 3, 'Hoenn'
    elif id in range(387,494):
        return 4, 'Sinnoh'
    elif id in range(494,650):
        return 5, 'Unova'
    elif id in range(650,722):
        return 6, 'Kalos'
    elif id in range(722,810):
        return 7, 'Alola'
    elif id in range(810,899):
        return 8, 'Galar'


def get_img_url(id):
    if id in [898, 897, 896, 895, 894, 893, 892, 891, 889, 888, 875, 849, 778, 774, 746, 745, 741, 718, 710, 648, 647, 642, 641, 586, 585, 392, 487, 413, 412]:
        return 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/' + str(id) + '.png'
    else:
        return 'https://pokeres.bastionbot.org/images/pokemon/' + str(id) + '.png'


def get3dList(pklist,n=3)->list:
    result_list = [pklist[i:i+n] for i in range(0, len(pklist), n)]
    return result_list

def get_home_page(request):
    context = {
        'types':types,
        'regions':regions,
        'generations':generations,
        'title': 'Home Page'
    }
    return render(request=request, template_name='home.html', context=context)

def get_all(request):
    all_pokemon_list = Pokemon.objects.all() 
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon':all_pokemon_list,
        'types':types,
        'regions':regions,
        'generations':generations,
        'title': 'All Pokemon'
    }
    return render(request=request, template_name='pokemonlist.html', context=context)


def get_pokemon_from_region(request, region_name):
    all_pokemon_list = Pokemon.objects.filter(region = region_name.capitalize() )
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon':all_pokemon_list,
        'types':types,
        'regions':regions,
        'generations':generations,
        'title': f'Region - {region_name.capitalize()}'
    }
    return render(request=request, template_name='pokemonlist.html', context=context)

def get_pokemon_from_generation(request, gid):
    all_pokemon_list = Pokemon.objects.filter(generation = gid)
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon':all_pokemon_list,
        'types':types,
        'regions':regions,
        'generations':generations,
        'title': f'Generation - {gid}'
    }
    return render(request=request, template_name='pokemonlist.html', context=context)

def get_pokemon_from_types(request, type_name):
    all_pokemon_list = Pokemon.objects.filter(type_name__type_name = type_name)
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon':all_pokemon_list,
        'types':types,
        'regions':regions,
        'generations':generations,
        'title': f'Types - {type_name.capitalize()}'
    }
    return render(request=request, template_name='pokemonlist.html', context=context)


def load_pokemon():
    total_pokemon_count = requests.get("https://pokeapi.co/api/v2/pokemon/").json().get('count')
    poke_api_url = "https://pokeapi.co/api/v2/pokemon/"
    for i in range(1,total_pokemon_count):
        response = requests.get(poke_api_url+str(i)).json()
        id = response.get('id')
        name = response.get('name').capitalize()
        height = response.get('height')/10
        weight = response.get('weight')/10
        image = get_img_url(id)
        generation, region = get_generation_and_region(id)
        poke = Pokemon(id=id, name=name, height=height, weight=weight, image=image, generation=generation, region=region)
        poke.save()        
        for x in response.get('types'):
            type_name = x.get('type').get('name')
            mType = Type.objects.get(type_name=type_name)
            poke.type_name.add(mType)
        poke.save()        
    print('pokemon data load success')


def load_types():
    response = requests.get("https://pokeapi.co/api/v2/type/").json()
    results = response.get('results')
    
    for index, i in enumerate(results):
        type = Type(index+1, type_name = i.get('name'))
        type.save()
    print('type data load success')


def load_data(request):
    # Type.objects.all().delete()
    # load_types()
    # Pokemon.objects.all().delete()
    # load_pokemon()
    return HttpResponse('Pokemon data loaded successfully')

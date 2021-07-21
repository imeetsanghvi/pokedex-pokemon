from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.shortcuts import render

from .models import Pokemon, Type

# Create your views here.

types = Type.objects.all()
regions = Pokemon.objects.order_by().values('region').distinct()
generations = Pokemon.objects.order_by().values('generation').distinct()
colors = {
    'grass': '#63BB5B',
    'fire': '#FF9C54',
    'water': '#4E90D5',
    'electric': '#F3D23B',
    'ice': '#74CEC0',
    'poison': '#AB6AC8',
    'ground': '#D97746',
    'rock': '#C7B78B',
    'bug': '#90C12C',
    'dragon': '#0A6DC4',
    'normal': '#f9199A1',
    'flying': '#8FA8DD',
    'fighting': '#D80A49',
    'psychic': '#F97176',
    'ghost': '#5269AC',
    'dark': '#5A5366',
    'steel': '#5A8EA1',
    'fairy': '#EC8FE6',
    'unknown': '#000000',
    'shadow': '#7D78A3'
}

type_logos = {
    'bug': 'https://upload.wikimedia.org/wikipedia/commons/3/3c/Pok%C3%A9mon_Bug_Type_Icon.svg',
    'dark': 'https://upload.wikimedia.org/wikipedia/commons/0/09/Pok%C3%A9mon_Dark_Type_Icon.svg',
    'dragon': 'https://upload.wikimedia.org/wikipedia/commons/a/a6/Pok%C3%A9mon_Dragon_Type_Icon.svg',
    'electric': 'https://upload.wikimedia.org/wikipedia/commons/a/a9/Pok%C3%A9mon_Electric_Type_Icon.svg',
    'fairy': 'https://upload.wikimedia.org/wikipedia/commons/0/08/Pok%C3%A9mon_Fairy_Type_Icon.svg',
    'fighting': 'https://upload.wikimedia.org/wikipedia/commons/b/be/Pok%C3%A9mon_Fighting_Type_Icon.svg',
    'fire': 'https://upload.wikimedia.org/wikipedia/commons/5/56/Pok%C3%A9mon_Fire_Type_Icon.svg',
    'flying': 'https://upload.wikimedia.org/wikipedia/commons/e/e0/Pok%C3%A9mon_Flying_Type_Icon.svg',
    'ghost': 'https://upload.wikimedia.org/wikipedia/commons/a/a0/Pok%C3%A9mon_Ghost_Type_Icon.svg',
    'grass': 'https://upload.wikimedia.org/wikipedia/commons/f/f6/Pok%C3%A9mon_Grass_Type_Icon.svg',
    'ground': 'https://upload.wikimedia.org/wikipedia/commons/8/8d/Pok%C3%A9mon_Ground_Type_Icon.svg',
    'ice': 'https://upload.wikimedia.org/wikipedia/commons/8/88/Pok%C3%A9mon_Ice_Type_Icon.svg',
    'normal': 'https://upload.wikimedia.org/wikipedia/commons/a/aa/Pok%C3%A9mon_Normal_Type_Icon.svg',
    'poison': 'https://upload.wikimedia.org/wikipedia/commons/c/c4/Pok%C3%A9mon_Poison_Type_Icon.svg',
    'psychic': 'https://upload.wikimedia.org/wikipedia/commons/a/ab/Pok%C3%A9mon_Psychic_Type_Icon.svg',
    'rock': 'https://upload.wikimedia.org/wikipedia/commons/b/bb/Pok%C3%A9mon_Rock_Type_Icon.svg',
    'steel': 'https://upload.wikimedia.org/wikipedia/commons/3/38/Pok%C3%A9mon_Steel_Type_Icon.svg',
    'water': 'https://upload.wikimedia.org/wikipedia/commons/0/0b/Pok%C3%A9mon_Water_Type_Icon.svg',
    'unknown': 'https://static.thenounproject.com/png/57788-200.png',
    'shadow': 'https://static.thenounproject.com/png/57788-200.png'
}


def get_generation_and_region(id):
    if id in range(1, 152):
        return 1, 'Kanto'
    elif id in range(152, 252):
        return 2, 'Johto'
    elif id in range(252, 387):
        return 3, 'Hoenn'
    elif id in range(387, 494):
        return 4, 'Sinnoh'
    elif id in range(494, 650):
        return 5, 'Unova'
    elif id in range(650, 722):
        return 6, 'Kalos'
    elif id in range(722, 810):
        return 7, 'Alola'
    elif id in range(810, 899):
        return 8, 'Galar'


def get_img_url(id):
    if id in [898, 897, 896, 895, 894, 893, 892, 891, 889, 888, 877, 875, 849, 778, 774, 746, 745, 741, 718, 710, 648, 647, 642, 641, 586, 585, 392, 487, 413, 412]:
        return 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/' + str(id) + '.png'
    else:
        return 'https://pokeres.bastionbot.org/images/pokemon/' + str(id) + '.png'


def get3dList(pklist, n=3) -> list:
    result_list = [pklist[i:i+n] for i in range(0, len(pklist), n)]
    return result_list


def get_home_page(request):
    context = {
        'types': types,
        'regions': regions,
        'generations': generations,
        'title': 'Home Page'
    }
    return render(request=request, template_name='home.html', context=context)


def get_all(request):
    all_pokemon_list = Pokemon.objects.all()
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon': all_pokemon_list,
        'types': types,
        'regions': regions,
        'generations': generations,
        'title': 'All Pokemon',
        'colors': colors
    }
    return render(request=request, template_name='pokemonlist.html', context=context)


def get_pokemon_from_region(request, region_name):
    all_pokemon_list = Pokemon.objects.filter(region=region_name.capitalize())
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon': all_pokemon_list,
        'types': types,
        'regions': regions,
        'generations': generations,
        'title': f'Region - {region_name.capitalize()}',
        'colors': colors
    }
    return render(request=request, template_name='pokemonlist.html', context=context)


def get_pokemon_from_generation(request, gid):
    all_pokemon_list = Pokemon.objects.filter(generation=gid)
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon': all_pokemon_list,
        'types': types,
        'regions': regions,
        'generations': generations,
        'title': f'Generation - {gid}',
        'colors': colors
    }
    return render(request=request, template_name='pokemonlist.html', context=context)


def get_pokemon_from_types(request, type_name):
    all_pokemon_list = Pokemon.objects.filter(type_name__type_name=type_name)
    all_pokemon_list = get3dList(all_pokemon_list)
    context = {
        'pokemon': all_pokemon_list,
        'types': types,
        'regions': regions,
        'generations': generations,
        'title': f'Types - {type_name.capitalize()}',
        'colors': colors
    }
    return render(request=request, template_name='pokemonlist.html', context=context)


def load_pokemon():
    total_pokemon_count = requests.get(
        "https://pokeapi.co/api/v2/pokemon/").json().get('count')
    poke_api_url = "https://pokeapi.co/api/v2/pokemon/"
    for i in range(1, total_pokemon_count):
        response = requests.get(poke_api_url+str(i)).json()
        id = response.get('id')
        name = response.get('name').capitalize()
        height = response.get('height')/10
        weight = response.get('weight')/10
        image = get_img_url(id)
        generation, region = get_generation_and_region(id)
        poke = Pokemon(id=id, name=name, height=height, weight=weight,
                       image=image, generation=generation, region=region)
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
        type_name = i.get('name')
        type_image = type_logos.get(type_name)
        type_color = colors.get(type_name)
        print(type_name, type_color, type_image)
        type = Type(index+1, type_name=type_name,
                    image=type_image, color=type_color)
        type.save()
    print('type data load success')


def load_data(request):
    # Type.objects.all().delete()
    # load_types()
    # Pokemon.objects.all().delete()
    # load_pokemon()
    return HttpResponse('Pokemon data loaded successfully')

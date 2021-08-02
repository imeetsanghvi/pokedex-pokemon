from django.db.models.query import QuerySet
from django.shortcuts import render
import requests
from django.http import HttpResponse
from django.shortcuts import render
from pokemon.filters import PokemonFilter
from .models import Pokemon, Regen, Type
import json
# Create your views here.

types = Type.objects.all()
generation = Regen.objects.all()
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
    'normal': '#FDEBD0',
    'flying': '#8FA8DD',
    'fighting': '#D80A49',
    'psychic': '#F97176',
    'ghost': '#8596c5',
    'dark': '#776d86',
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

context = {
    'types': types,
    'generation':generation,
}

def get_generation_and_region(id):
    if id in range(1, 152):
        gen = 1
    elif id in range(152, 252):
        gen = 2
    elif id in range(252, 387):
        gen = 3
    elif id in range(387, 494):
        gen = 4
    elif id in range(494, 650):
        gen = 5
    elif id in range(650, 722):
        gen = 6
    elif id in range(722, 810):
        gen = 7
    elif id in range(810, 899):
        gen = 8
    return Regen.objects.get(gen = gen)


def get_img_url(id):
    if id in [898, 897, 896, 895, 894, 893, 892, 891, 889, 888, 877, 875, 849, 778, 774, 746, 745, 741, 718, 710, 648, 647, 642, 641, 586, 585, 392, 487, 413, 412]:
        return 'https://assets.pokemon.com/assets/cms2/img/pokedex/full/' + str(id) + '.png'
    else:
        return 'https://pokeres.bastionbot.org/images/pokemon/' + str(id) + '.png'


def get3dList(pklist, n=3) -> list:
    result_list = [pklist[i:i+n] for i in range(0, len(pklist), n)]
    return result_list


def get_home_page(request):
    context['title'] = 'Pokedex'
    return render(request=request, template_name='home.html', context=context)


# def get_developer(request):
#     links = [
#         ['bi bi-github','Github','https://github.com/imeetsanghvi', 'imeetsanghvi'],
#         ['bi bi-linkedin','LinkedIn','https://linkedin.com/in/imeetsanghvi', 'imeetsanghvi'],
#         ['bi bi-code-slash','Leet Code','https://linkedin.com/in/imeetsanghvi', 'imeetsanghvi'],
#         ['bi bi-code-slash','HackerRank','https://linkedin.com/in/imeetsanghvi', 'imeetsanghvi'],
#         ['bi bi-youtube','Youtube', 'https://youtube.com/c/meetsanghvi', 'meetsanghvi'],
#         ['bi bi-instagram','Instagram', 'https://instagram.com/imeetsanghvi', 'imeetsanghvi'],
#         ['bi bi-facebook','Facebook', 'https://facebook.com/imeetsanghvi', 'imeetsanghvi'],
#         ['bi bi-twitter','Twitter', 'https://twitter.com/imeetsanghvi', 'imeetsanghvi'],
#     ]
#     context['title'] = 'Developer'
#     context['links'] = links
#     return render(request=request, template_name='developer-contact.html', context=context)


# pokemon fetch and queries
def get_all(request):
    pokemon_list = Pokemon.objects.all()
    # req = dict(request.GET.items())
    req = request
    # print(req.GET)
    
    name = req.GET.get('name')
    type_name = req.GET.getlist('type_name')
    
    regen = req.GET.getlist('regen')
    # print(regen)
    type_name = [type for type in type_name if len(type)!=0]
    regen = [int(gen) for gen in regen]
    # print(name, type_name, regen)
    if name not in [None, ""]:
        pokemon_list = pokemon_list.filter(name__icontains=name.capitalize())
    if len(type_name)!=0:
        pokemon_list = pokemon_list.filter(type_name__id__in = type_name)
    if len(regen)!=0:
        pokemon_list = pokemon_list.filter(regen__gen__in = regen)
            
    filtered_pokemon = PokemonFilter(request=request, queryset=pokemon_list)
    pokemon =  get3dList(filtered_pokemon.qs)
    
    context['filtered_pokemon'] = filtered_pokemon
    context['pokemon'] = pokemon
    context['title'] = 'Pokemon'
    return render(request=request, template_name="pokemonlist.html", context=context)



# working with the models and data set
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
        # regen = get_generation_and_region(id)
        
        poke = Pokemon(id=id, name=name, height=height, weight=weight, image=image )
        poke.save()
        
        for x in response.get('types'):
            type_name = x.get('type').get('name')
            mType = Type.objects.get(type_name=type_name)
            poke.type_name.add(mType)
        
        poke.save()
        
    print('pokemon data load success')


def add_pokemon_regen():
    pokemon = Pokemon.objects.all()
    for poke in pokemon:
        regen = get_generation_and_region(poke.id)
        poke.regen.add(regen)
        poke.save()
        print(poke)


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
    

def load_regen():
    regen = {
        1: "Kanto",
        2: "Johto",
        3: "Hoenn",
        4: "Sinnoh",
        5: "Unova",
        6: "Kalos",
        7: "Alola",
        8: "Galar",
    }
    
    for gen, reg in regen.items():
        Regen(gen = gen, reg = reg).save()
    print(Regen.objects.all())
    
    return HttpResponse('Pokemon region data loaded successfully')


def load_pokemon_images():
    pokemon = Pokemon.objects.all()
    for poke in pokemon:
        print(poke.id)
        
        img_url = f"https://assets.pokemon.com/assets/cms2/img/pokedex/full/{str(poke.id).zfill(3)}.png"
        poke.image = img_url
        poke.save()
        # print(poke)
        
def load_data(request):
    # Type.objects.all().delete()
    # load_types()
    
    # Regen.objects.all().delete()
    # Regen.objects
    # load_regen()
    
    # Pokemon.objects.all().delete()
    # load_pokemon()
    
    # add_pokemon_regen()
    # print('do some procesing')
    
    # load_pokemon_images()
    
    return HttpResponse('Pokemon data loaded successfully')

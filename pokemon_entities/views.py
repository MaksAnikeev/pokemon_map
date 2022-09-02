import folium
import json
import os

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime
from pprint import pprint

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    current_time = localtime()
    entity_pokemons = PokemonEntity.objects.filter(appeared_at__lt=current_time,
                                                   disappeared_at__gt=current_time)
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity_pokemon in entity_pokemons:
            add_pokemon(folium_map,
                        entity_pokemon.lat,
                        entity_pokemon.lon,
                        os.path.join('media', f'{entity_pokemon.pokemon.photo}'))

    my_pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in my_pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(f'/media/{pokemon.photo}'),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    # with open('pokemon_entities/pokemons.json', encoding='utf-8') as database:
    #     pokemons = json.load(database)['pokemons']
    # for pokemon in pokemons:
    #     if pokemon['pokemon_id'] == int(pokemon_id):
    #         requested_pokemon = pokemon
    #         break
    # else:
    #     return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon_params = Pokemon.objects.get(pk=pokemon_id)
    pokemon = {
            'pokemon_id': pokemon_params.id,
            'title_ru': pokemon_params.title,
            'title_en': pokemon_params.title_en,
            'title_jp': pokemon_params.title_jp,
            'description': pokemon_params.description,
            'img_url': request.build_absolute_uri(f'/media/{pokemon_params.photo}')
                }
    current_time = localtime()
    entity_pokemons = PokemonEntity.objects.filter(pokemon__id = pokemon_id,
                                                   appeared_at__lt=current_time,
                                                   disappeared_at__gt=current_time
                                                   )
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for entity_pokemon in entity_pokemons:
        add_pokemon(folium_map,
                    entity_pokemon.lat,
                    entity_pokemon.lon,
                    os.path.join('media', f'{entity_pokemon.pokemon.photo}'))
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
# {'pokemon_id': 1, 'img_url': 'media\\bulbazavr_ZWjN8ek.png', 'title_ru': 'Бульбазавр'}
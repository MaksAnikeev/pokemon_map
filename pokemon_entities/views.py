import folium
import os

from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils.timezone import localtime

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
    folium_map = folium.Map(location=MOSCOW_CENTER,
                            zoom_start=12)
    for entity_pokemon in entity_pokemons:
        add_pokemon(folium_map,
                    entity_pokemon.lat,
                    entity_pokemon.lon,
                    request.build_absolute_uri(f'/media/{entity_pokemon.pokemon.photo}'))

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon.photo.url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon_params = get_object_or_404(Pokemon, pk=pokemon_id)
    if pokemon_params.previous_evolution:
        previous_evolution = {"title_ru": pokemon_params.previous_evolution.title,
                              "pokemon_id": pokemon_params.previous_evolution.id,
                              "img_url": pokemon_params.previous_evolution.photo.url
                              }
    else:
        previous_evolution = {}

    next_evolution_params = pokemon_params.next_evolutions.all().first()
    if next_evolution_params:
        next_evolution = {"title_ru": next_evolution_params.title,
                          "pokemon_id": next_evolution_params.id,
                          "img_url": next_evolution_params.photo.url
                          }
    else:
        next_evolution = {}

    pokemon = {
        'pokemon_id': pokemon_params.id,
        'title_ru': pokemon_params.title,
        'title_en': pokemon_params.title_en,
        'title_jp': pokemon_params.title_jp,
        'description': pokemon_params.description,
        'img_url': pokemon_params.photo.url,
        "previous_evolution": previous_evolution,
        "next_evolution": next_evolution
    }
    current_time = localtime()
    pokemon_entities = PokemonEntity.objects.filter(pokemon__id=pokemon_id,
                                                   appeared_at__lt=current_time,
                                                   disappeared_at__gt=current_time
                                                   )
    folium_map = folium.Map(location=MOSCOW_CENTER,
                            zoom_start=12)
    for pokemon_entity in pokemon_entities:
        add_pokemon(folium_map,
                    pokemon_entity.lat,
                    pokemon_entity.lon,
                    request.build_absolute_uri(f'/media/{pokemon_entity.pokemon.photo}'))
    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })

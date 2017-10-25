import dbutils
import functools
import os
import re
import requests
import itertools

STEAM_API_KEY = '576C821F7F6F425E341F9955224C9FEE'
DATABASE_PATH = os.getenv('DB_PATH', './data.db')


def parseUrl(url):
    '''
    Given a url of the form
        steamcommunity.com/id/<vanity_id> 
    or
        steamcommunity.com/profiles/<steam_id>
    Returns the user identifier (either a steamid or a vanity_id)
    and a bool indicated whether it is a steamid or not.
    '''

    if url.endswith('/'):
        url = url[:-1]
    urlList = url.split('/')
    if len(urlList) < 2:
        raise CannotDetermineSteamId(url)

    id_or_profile = urlList[-2]
    steamid_or_vanityid = urlList[-1]
    return steamid_or_vanityid, id_or_profile != 'id'

@functools.lru_cache(maxsize=128)
def resolve_vanity_id(vanity_id):
    request = requests.get('https://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/',
                 params={
                     'key': STEAM_API_KEY,
                     'vanityurl': vanity_id,
                 })
    if not request or request.json().get('response', {}).get('message', '').lower() == 'no match':
        raise CannotDetermineSteamId(vanity_id)
    return request.json()['response']['steamid']

@functools.lru_cache(maxsize=128)
def get_games_owned_by_user_web(user_steamid, include_free=False):
    include_free = 'true' if include_free else 'false'
    parameters = {
        'key': STEAM_API_KEY,
        'steamid': user_steamid,
        'include_appinfo': 'true',
        'include_played_free_games': include_free
    }
    request = requests.get('https://api.steampowered.com/IPlayerService/GetOwnedGames/v1',
                        params=parameters)

    return [appid_playtime_entry['appid']
            for appid_playtime_entry
            in request.json()['response']['games']]


def get_cached_user_summaries(steamids):
    return dbutils.get_cached_md_for_users(steamids, DATABASE_PATH)

def get_user_summaries(steamids):
    user_summaries, cache_misses = get_cached_user_summaries(steamids)

    fetched_misses = [ get_user_summary_web(steamid) for steamid in cache_misses ]

    dbutils.storeUserDatas(fetched_misses, DATABASE_PATH)

    return itertools.chain(user_summaries, cache_misses)


@functools.lru_cache(maxsize=16384)
def get_user_summary_web(user_steamid):
    request = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002',
                           params={
                               'key': STEAM_API_KEY,
                               'steamids': user_steamid,
                           })
    user_data = request.json()['response']['players'][0]

    return {
        'steamid': user_data.get('steamid'),
        'avatar': user_data.get('avatarfull'),
        'username': user_data.get('personaname'),
        'profile_url': user_data.get('profileurl'),
        'name': user_data.get('realname'),
    }

def get_datas_for_game_web(appid):
    steamspy_request = requests.get('https://steamspy.com/api.php',
                                    params={
                                        'request': 'appdetails',
                                        'appid': appid,
                                    })
    steamspy_data = steamspy_request.json()

    steam_request = requests.get('http://store.steampowered.com/api/appdetails',
                                 params={
                                     'key': STEAM_API_KEY,
                                     'appids': appid,
                                 })
    if steam_request:
        steam_data = steam_request.json().get(str(appid), {}).get('data', {})
        return (steam_data, steamspy_data)
    else:
        return None, None

@functools.lru_cache(maxsize=16384)
def get_formatted_data_for_game(appid):
    steam_data, steamspy_data = get_datas_for_game_web(appid)
    return consolidate_game_data(appid, steam_data, steamspy_data)


def get_cached_game_datas(appids):
    return dbutils.get_cached_md_for_games(appids, DATABASE_PATH)

def get_data_for_games(appids):
    cached_game_datas, cache_misses = get_cached_game_datas(appids)
    
    fetched_misses = ( get_formatted_data_for_game(appid) for appid in cache_misses )

    fetched_misses = filter(lambda x: x,fetched_misses)
    all_fetched = []
    fetched_batch = []

    for fetched_data in fetched_misses:
        all_fetched.append(fetched_data)
        fetched_batch.append(fetched_data)

        if len(fetched_batch) > 30:
            dbutils.storeGameDatas(fetched_batch, DATABASE_PATH)
            fetched_batch = []

    if fetched_batch:
        dbutils.storeGameDatas(fetched_batch, DATABASE_PATH)

    return itertools.chain(cached_game_datas, fetched_misses)

def derive_store_page_from_appid(appid):
    return 'http://store.steampowered.com/app/' + str(appid)

def is_game_multiplayer(steam_data={}, steamspy_data={}):
    steam_multiplayer_categories = {
        'multi-player',
        'co-op',
    }

    for category_entry in steam_data.get('categories', []):
        if category_entry['description'].lower() in steam_multiplayer_categories:
            return True

    steam_multiplayer_tags = {
        'multi-player',
        'multiplayer',
        'local multiplayer',
        'online multiplayer',
        'co-op',
        'local co-op',
        'online co-op',
        '4 player local',
        'split screen',
    }

    tags = steamspy_data.get('tags', {})
    if isinstance(tags, dict):
        tags = tags.keys()
    for tag in tags:
        if tag.lower() in steam_multiplayer_tags:
            return True

    return False


def consolidate_game_data(appid, steam_data, steamspy_data):
    if not steam_data and steamspy_data:
        return None
    
    platforms = [platform.capitalize()
                 for (platform, is_on)
                 in steam_data.get('platforms', {}).items()
                 if is_on]

    genres = [genre_entry['description'].capitalize()
              for genre_entry
              in steam_data.get('genres', [])]

    store_page = derive_store_page_from_appid(appid)

    price = steam_data.get('price_overview', {}).get('initial') or steam_data.get('price_overview', {}).get('final')

    tags = steamspy_data.get('tags', [])
    if isinstance(tags, dict):
        tags = list(tags.keys())

    return { # Example data for Dungeon Defenders
        'name': steam_data.get('name'),                         # 'Dungeon Defenders'
        'appid': appid,                                         # 65800
        'image': steam_data.get('header_image'),                # https://etc...
        'platforms': platforms,                                 # ['Windows', 'Linux', ...]
        'genres': genres,                                       # ['Action', 'Indie', ...]
        'tags': tags,                                           # ['Tower Defense', 'RPG', ...]
        'global_owners': steamspy_data.get('owners'),           # 2046279
        'developer': steamspy_data.get('developer'),            # 'Trendy Entertainment'
        'publisher': steamspy_data.get('publisher'),            # 'Trendy Entertainment'
        'store_page': store_page,                               # https://etc...
        'price': price,                                         # 1599
        'multiplayer': is_game_multiplayer(steam_data, steamspy_data),
    }

def intersect_game_lists(game_lists):
    first_list, *rest = game_lists
    if not rest:
        return first_list
    else:
        first_set = set(first_list)
        rest_sets = map(set, rest)
        return first_set.intersection(*rest_sets)

class CannotDetermineSteamId(Exception):
    pass



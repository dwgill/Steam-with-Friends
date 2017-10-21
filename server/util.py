import requests
import re
import functools

STEAM_API_KEY = '576C821F7F6F425E341F9955224C9FEE'

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
        raise Exception('Invalid Steam profile url: ' + url)

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
    return request.json()['response']['steamid']

@functools.lru_cache(maxsize=128)
def get_games_owned_by_user(user_steamid, include_free=False):
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


@functools.lru_cache(maxsize=16384)
def get_user_summary(user_steamid):
    request = requests.get('https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002',
                           params={
                               'key': STEAM_API_KEY,
                               'steamids': user_steamid,
                           })

    return request.json()['response']['players'][0]

@functools.lru_cache(maxsize=16384)
def get_game_datas(appid):
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
    steam_data = steam_request.json()[str(appid)].get('data', {})

    return (steam_data, steamspy_data)


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


def consolidate_game_data(steam_data, steamspy_data):
    platforms = [platform.capitalize()
                 for (platform, is_on)
                 in steam_data.get('platforms', {}).items()
                 if is_on]

    genres = [genre_entry['description'].capitalize()
              for genre_entry
              in steam_data.get('genres', [])]

    store_page = derive_store_page_from_appid(steamspy_data.get('appid'))

    return { # Example data for Dungeon Defenders
        'name': steam_data.get('name'),                         # 'Dungeon Defenders'
        'appid': steam_data.get('steam_appid',                  # 65800
                                steamspy_data.get('appid')),
        'image': steam_data.get('header_image'),                # https://etc...
        'platforms': platforms,                                 # ['Windows', 'Linux', ...]
        'genres': genres,                                       # ['Action', 'Indie', ...]
        'tags': list(steamspy_data.get('tags', {}).keys()),     # ['Tower Defense', 'RPG', ...]
        'global_owners': steamspy_data.get('owners'),           # 2046279
        'developer': steamspy_data.get('developer'),            # 'Trendy Entertainment'
        'publisher': steamspy_data.get('publisher'),            # 'Trendy Entertainment'
        'store_page': store_page,                               # https://etc...
        'price': steam_data.get('price_overview', {}).get('final'), # 1599
    }

def intersect_game_lists(game_lists):
    first_list, *rest = game_lists
    if not rest:
        return first_list
    else:
        first_set = set(first_list)
        rest_sets = (set(game_list) for game_list in rest)
        return first_set.intersection(*rest_sets)


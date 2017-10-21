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
def get_game_info(gameid):
    steamspy_request = requests.get('https://steamspy.com/api.php',
                           params={
                               'request': 'appdetails',
                               'appid': gameid,
                           }).json()

    steam_request = requests.get('http://store.steampowered.com/api/appdetails',
                                 params={
                                     'key': STEAM_API_KEY,
                                     'appids': gameid,
                                 }).json()


    return request.json()

def intersect_game_lists(game_lists):
    first_list, *rest = game_lists
    if not rest:
        return first_list
    else:
        first_set = set(first_list)
        rest_sets = (set(game_list) for game_list in rest)
        return list(first_set.intersection(*rest_sets))


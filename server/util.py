import requests
import re

STEAM_API_KEY = '576C821F7F6F425E341F9955224C9FEE'

def parseUrl(url):
    urlList = url.split('/')
    idDetector = urlList[len(urlList) - 2]
    idName = urlList[len(urlList) - 1]
    return idDetector ,idName

def resolve_vanity_id(vanity_id):
    return requests.get('http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/',
                 params={
                     'key': STEAM_API_KEY,
                     'vanityurl': vanity_id,
                 }).json()['response']['steamid']

steam_profile_re = re.compile(r'(https?://)?steamcommunity.com/((profiles/(?P<steam_id>[0-9]+))|(id/(?P<vanity_id>[a-zA-Z0-9]+)))')
def get_user_id_from_url(profile_url):
    match = steam_profile_re.match(profile_url)
    if match:
        if match.group('steam_id'):
            return match.group('steam_id')
        else:
            vanity_id = match.group('vanity_id')
            return resolve_vanity_id(vanity_id)
    else:
        return None

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

    return request.json()['response']

def get_user_summary(user_steamid):
    return requests.get('http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002',
                 params={
                    'key': STEAM_API_KEY,
                     'steamids': user_steamid,
                 }).json()['response']['players'][0]

def get_all_user_data(user_steamid, include_free_games=False):
    user_info = get_user_summary(user_steamid)
    games_info = get_games_owned_by_user(user_steamid, include_free_games)
    return {
        'user': user_info,
        'games': games_info['games'],
        'games_count': games_info['game_count'],
    }

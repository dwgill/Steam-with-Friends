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

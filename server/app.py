from flask import Flask, request, jsonify
import util
import dbutils
import os

app = Flask(__name__)

if os.getenv('ENV', '') == 'DEV':
    from flask_cors import CORS
    cors = CORS(app, resources={r"/get-games*": {"origins": "*"}})

def error(msg, status=400):
    return jsonify({
        'status': 'error',
        'error': msg,
    }), status

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-games')
def get_games():
    if not request.args.get('users'):
        return error('no arguments')
    params = request.args.get('users').split(',')

    if not params:
        return error('no arguments')

    try: 
        params = (parse_param(param) for param in params)

        steamids = [identifier if is_steam_id else util.resolve_vanity_id(identifier)
                    for (identifier, is_steam_id)
                    in params]
    except util.CannotDetermineSteamId as err:
        return error('cannot determine steamid: ' + str(err))

    user_summaries = util.get_user_summaries(steamids)

    lists_of_appids = [util.get_games_owned_by_user_web(steamid) for steamid in steamids]

    games_owned_by_all = util.intersect_game_lists(lists_of_appids)

    games_owned_by_all = util.get_data_for_games(games_owned_by_all)

    multi_games_owned_by_all = filter(lambda gdata: gdata['multiplayer'], games_owned_by_all)


    return jsonify({
        'users': list(user_summaries),
        'games': list(multi_games_owned_by_all),
        'status': 'success',
    })

def parse_param(param):
    param = str(param)
    param = param.replace('http://', '').replace('https://', '')

    if param.isdecimal():
        return (param, True)
    elif param.isalnum():
        return (param, False)
    elif param.startswith('steamcommunity.com/'):
        return util.parseUrl(param)
    else:
        raise util.CannotDetermineSteamId(Param)

if __name__ == '__main__':
    if os.getenv('ENV', '') == 'DEV':
        app.run(debug=True)
    else:
        app.run()


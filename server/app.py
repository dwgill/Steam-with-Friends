from flask import Flask, request, jsonify
from flask_cors import CORS
import util
import dbutils

app = Flask(__name__)
cors = CORS(app, resources={r"/get-games*": {"origins": "*"}})

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-games')
def get_games():
    if not request.args.get('users'):
        return jsonify([]);
    params = request.args.get('users').split(',')

    params = (parse_param(param) for param in params)

    steamids = (identifier if is_steam_id else util.resolve_vanity_id(identifier)
                for (identifier, is_steam_id)
                in params)

    users_and_games = ( (util.get_user_summary(steamid), util.get_games_owned_by_user_web(steamid))
             for steamid in steamids)

    users, game_lists = zip(*users_and_games)

    games_owned_by_all = util.intersect_game_lists(game_lists)

    games_owned_by_all = util.get_data_for_games(games_owned_by_all)

    multi_games_owned_by_all = filter(lambda gdata: gdata['multiplayer'], games_owned_by_all)


    return jsonify({
        'users': users,
        'games': list(multi_games_owned_by_all),
    })

def parse_param(param):
    param = param.replace('http://', '').replace('https://', '')

    if param.isdecimal():
        return (param, True)
    elif param.isalnum():
        return (param, False)
    elif param.startswith('steamcommunity.com/'):
        return util.parseUrl(param)
    else:
        raise Exception('Invalid parameter: ' + param)


if __name__ == '__main__':
    app.run()


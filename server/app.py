from flask import Flask, request, jsonify
from flask_cors import CORS
import util
app = Flask(__name__)
cors = CORS(app, resources={r"/get-games*": {"origins": "*"}})
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-games')
def get_game():
    steam_ids = map(util.get_user_id_from_url, request.args.get('userProfiles').split(','))
    data = map(util.get_all_user_data, steam_ids)

    return jsonify(list(data))

if __name__ == '__main__':
    app.run()


from flask import Flask, request, jsonify
import util
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-games')
def get_game():
    profiles = list(map(util.get_user_id_from_url, request.args.get('userProfiles').split(',')))
    return jsonify(profiles)

if __name__ == '__main__':
    app.run()

from dotenv import dotenv_values
from pymongo import MongoClient
from flask import Flask, Response
from flask_cors import CORS, cross_origin
from flask import request
from recommender.neo4jquery import OntologyRecomendations
import json
import controller

# Load neo4j database
neo_db = OntologyRecomendations("bolt://localhost:8001")
# Load mongodb credentials
config = dotenv_values(".env")
username = config['USER']
key = config['PASSWORD']
# connect to MongoDB
client = MongoClient(f"mongodb+srv://{username}:{key}@cluster0.hynxe.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=client.taller
movies_col = db['movies']
users_col = db['users']

app = Flask(__name__)
CORS(app)

@app.route('/login/<userId>', methods=['GET'])
@cross_origin()
def login(userId=None):
    user_data = controller.get_user_by_id(users_col, userId)
    if not user_data:
        return Response(json.dumps({ 'msg': 'Access Denied' }), status=401, mimetype='application/json')
    else:
        return Response(json.dumps(user_data), status=200, mimetype='application/json')

@app.route('/signup/<userId>', methods=['GET'])
@cross_origin()
def login(userId=None):
    user_data = controller.create_user_with_id(users_col, userId)
    if not user_data:
        return Response(json.dumps({ 'msg': 'Failed to create' }), status=401, mimetype='application/json')
    else:
        return Response(json.dumps(user_data), status=200, mimetype='application/json')

@app.route('/movie/<movieId>', methods=['GET'])
@cross_origin()
def get_movie(movieId=None):
    movie_data = controller.find_movie_by_id(movies_col, movieId)
    if not movie_data:
        return Response(json.dumps({ 'msg': 'No movie was found' }), status=404, mimetype='application/json')
    else:
        return Response(json.dumps(movie_data), status=200, mimetype='application/json')

@app.route('/movies', methods=['GET'])
@cross_origin()
def find_movies():
    partial_name = request.args.get('partial_name')
    page = 0
    if "page_num" in request.args:
        try:
            page = int(request.args.get('page_num'))
        except:
            page = 0
    results_list = controller.find_movies_with_partial(movies_col, partial_name, page, 100)
    return Response(json.dumps(results_list), status=200, mimetype='application/json')

@app.route('/top', methods=['GET'])
@cross_origin()
def get_top_movies():
    results_list = controller.find_top_movies(movies_col, 10)
    return Response(json.dumps(results_list), status=200, mimetype='application/json')

@app.route('/history/<userId>', methods=['GET'])
@cross_origin()
def get_user_history(userId=""):
    results_list = controller.get_history(movies_col, users_col, userId)
    return Response(json.dumps(results_list), status=200, mimetype='application/json')

@app.route('/recommendations/<userId>', methods=['GET'])
@cross_origin()
def get_recommedations(userId=""):
    results_list = controller.get_recommedations(movies_col, users_col, neo_db, userId)
    return Response(json.dumps(results_list), status=200, mimetype='application/json')

@app.route('/push/<userId>', methods=['GET'])
@cross_origin()
def update_recommendatons(userId=""):
    controller.update_recom_window(users_col, userId)
    return Response(json.dumps({ 'msg': 'Updated'}), status=200, mimetype='application/json')

@app.route('/like', methods=['POST'])
@cross_origin()
def like_movie():
    req_data = request.json
    userId = req_data['userId']
    movieId = req_data['movieId']
    controller.like_movie(users_col, movies_col, userId, movieId)
    return Response(json.dumps({ 'msg': 'Updated'}), status=200, mimetype='application/json')

@app.route('/dislike', methods=['POST'])
@cross_origin()
def dislike_movie():
    req_data = request.json
    userId = req_data['userId']
    movieId = req_data['movieId']
    controller.dislike_movie(users_col, userId, movieId)
    return Response(json.dumps({ 'msg': 'Updated'}), status=200, mimetype='application/json')

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=True, host="0.0.0.0", port=5000)
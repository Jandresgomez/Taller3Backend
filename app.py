from dotenv import dotenv_values
from pymongo import MongoClient
from flask import Flask, Response
from flask_cors import CORS, cross_origin
from flask import request
import json
import controller

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
    user_data = controller.getUserByUserId(users_col, userId)
    if not user_data:
        return Response(json.dumps({ 'msg': 'Access Denied' }), status=401, mimetype='application/json')
    else:
        return Response(json.dumps(user_data), status=200, mimetype='application/json')

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

if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=True, host="0.0.0.0", port=5000)
import json
from flask import Flask, request, jsonify
from main import search_from_client
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return json.dumps({'msg': 'api is running...'})


@app.route('/api/query', methods=['POST'])
def query():
    body = json.loads(request.data)
    print(body['query'])
    links = search_from_client(body['query'])
    return jsonify({"links":links})
    
    

app.run() #runs on port 5000 by default


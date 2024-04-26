from park_mgmt import *
from flask import Flask,request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

@app.route('/park', methods = ['POST'])
def park():

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    log_park(data['user_id'], 
             data['car_id'],
             data['location'])
    
    return jsonify({
        "message": "Successfully parked user!"
    }), 200

@app.route('/leave', methods = ['POST'])
def leave():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    data = request.get_json()

    leave_park(data['user_id'],
               data['car_id'])
    
    return jsonify({
        "message": "User successfully left parking space!"
    }), 200


if __name__ == '__main__':
    app.run(debug=True)


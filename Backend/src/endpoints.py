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

@app.route('/check-parked', methods = ['GET'])
def isPark():
    user_id = request.args.get('user_id')
    car_id = request.args.get('car_id')
    
    if not user_id or not car_id:
        return jsonify({"error": "Missing user_id or car_id"}), 400
    
        
    parked, location = check_park(int(user_id), int(car_id))

    
    if parked:
        return jsonify({"isParked": True, "location": location}), 200
    else:
        return jsonify({"isParked": False}), 200

@app.route('/get-parked-cars', methods=['GET'])
def get_parked_cars():
    # Retrieve parameters from URL query
    sw_lat = request.args.get('sw_lat', type=float)
    sw_lon = request.args.get('sw_lon', type=float)
    ne_lat = request.args.get('ne_lat', type=float)
    ne_lon = request.args.get('ne_lon', type=float)

    if None in [sw_lat, sw_lon, ne_lat, ne_lon]:
        return jsonify({"error": "Missing coordinates parameters"}), 400

    # Fetch parked car positions
    results = load_parks(sw_lat, sw_lon, ne_lat, ne_lon)


    return jsonify(results)



if __name__ == '__main__':
    app.run(debug=True)






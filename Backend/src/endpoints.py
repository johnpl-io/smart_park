from park_mgmt import *
from user_mgmt import *
from car_mgmt import *
from flask import Flask,request, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
CORS(app, support_credentials=True)

@app.route('/park', methods = ['POST'])
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
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
@cross_origin(supports_credentials=True)
def get_parked_cars():
    # Retrieve parameters from URL query
    sw_lat = request.args.get('sw_lat', type=float)
    sw_lon = request.args.get('sw_lon', type=float)
    ne_lat = request.args.get('ne_lat', type=float)
    ne_lon = request.args.get('ne_lon', type=float)

    if None in [sw_lat, sw_lon, ne_lat, ne_lon]:
        return jsonify({"error": "Missing coordinates parameters"}), 400

    # Fetch parked car positions
    heatmap_img, bounds = load_parks(sw_lat, sw_lon, ne_lat, ne_lon)

    return jsonify({"image": heatmap_img, "bounds":bounds})

@app.route('/find-user-by-email', methods = ['GET'])
@cross_origin(supports_credentials=True)
def find_user():

    email = request.args.get('email')
    exists, username, user_id = user_lookup(email)

    return jsonify({"exists": exists, "username": username, "user_id": user_id})

@app.route('/check-username', methods = ['GET'])
@cross_origin(supports_credentials=True)
def check_username():
    username = request.args.get('username')
    
    exists = user_exists(username)

    return jsonify({"exists": exists})

@app.route('/create-user', methods = ['POST'])
@cross_origin(supports_credentials=True)
def make_user():

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()
    
    create_user(data["username"], 
                data["email_address"],
                data["hashed_password"])

    return jsonify({
        "message": "Successfully created user!"
    }), 200

@app.route('/get-cars', methods = ['GET'])
@cross_origin(supports_credentials=True)
def get_users_cars():
    user_id = request.args.get('user_id', type = int)

    cars = get_cars(user_id)

    return jsonify({"cars": cars})

@app.route('/get-models', methods = ['GET'])
@cross_origin(supports_credentials=True)
def get_car_models():

    car_models = get_models()

    return jsonify({"car_models": car_models})


@app.route('/search-cars', methods = ['GET'])
@cross_origin(supports_credentials=True)
def search_car():

    search_term = request.args.get('search_term')
    cars = find_cars(search_term)

    return jsonify({"cars": cars})

@app.route('/register-car', methods = ['POST'])
@cross_origin(supports_credentials=True)
def register_car():

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    register(int(data["user_id"]),
                  int(data["car_id"]))
    
    


if __name__ == '__main__':
    app.run(debug=True)






from park_mgmt import Park_MGMT
from user_mgmt import User_MGMT
from car_mgmt import Car_MGMT
from park_finder_mgmt import ParkFinder_MGMT
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from geojson import Point
from sqlalchemy import create_engine

app = Flask(__name__)
CORS(app, support_credentials=True)
engine_str = "postgresql+psycopg2://user:password@localhost:5432/smart_park_db"
engine = create_engine(engine_str)
# Initialize the management classes
park_mgmt = Park_MGMT(engine=engine)
user_mgmt = User_MGMT(engine=engine)
car_mgmt = Car_MGMT(engine=engine)
park_finder_mgmt = ParkFinder_MGMT(engine=engine)


@app.route("/park", methods=["POST"])
@cross_origin(supports_credentials=True)
def park():

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    print(data["location"])
    # flipping the coordinates for backend
    backend_location = (data["location"][1], data["location"][0])

    print(backend_location)
    park_mgmt.log_park(int(data["user_id"]), int(data["car_id"]), backend_location)

    return jsonify({"message": "Successfully parked user!"}), 200


@app.route("/leave", methods=["POST"])
@cross_origin(supports_credentials=True)
def leave():
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    park_mgmt.leave_park(data["user_id"], data["car_id"])

    return jsonify({"message": "User successfully left parking space!"}), 200


@app.route("/check-parked", methods=["GET"])
@cross_origin(supports_credentials=True)
def isPark():
    user_id = request.args.get("user_id")
    car_id = request.args.get("car_id")

    if not user_id or not car_id:
        return jsonify({"error": "Missing user_id or car_id"}), 400

    parked, location = park_mgmt.check_park(int(user_id), int(car_id))

    # flipping the coordinates for frontend
    if location:
        location = (location[1], location[0])

    if parked:
        return jsonify({"isParked": True, "location": location}), 200
    else:
        return jsonify({"isParked": False}), 200


@app.route("/get-parked-cars", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_parked_cars():
    # Retrieve parameters from URL query
    sw_lat = request.args.get("sw_lat", type=float)
    sw_lon = request.args.get("sw_lon", type=float)
    ne_lat = request.args.get("ne_lat", type=float)
    ne_lon = request.args.get("ne_lon", type=float)

    if None in [sw_lat, sw_lon, ne_lat, ne_lon]:
        return jsonify({"error": "Missing coordinates parameters"}), 400

    # Fetch parked car positions
    heatmap_img, bounds = park_mgmt.load_parks(sw_lat, sw_lon, ne_lat, ne_lon)

    return jsonify({"image": heatmap_img, "bounds": bounds})


@app.route("/find-closest-free-spot")
# returns a list of ten recently free spots
def find_closest_free_spot():
    user_id = request.args.get("user_id", type=int)
    car_id = request.args.get("car_id", type=int)
    lon = request.args.get("lon", type=float)
    lat = request.args.get("lat", type=float)
    park_results = park_finder_mgmt.park_find(user_id, car_id, [lon, lat])
    #  breakpoint()
    # convert to geojson
    spots = []
    for spot in park_results:
        spots.append(
            {
                "spot_id": spot[0],
                "location": Point((spot[2], spot[1])),
                "distance": spot[3],
                "time_left": spot[4],
            }
        )

    return jsonify(spots)


@app.route("/find-user-by-email", methods=["GET"])
@cross_origin(supports_credentials=True)
def find_user():

    email = request.args.get("email")
    exists, username, user_id = user_mgmt.user_lookup(email)
    return jsonify({"exists": exists, "username": username, "user_id": user_id})


@app.route("/check-username", methods=["GET"])
@cross_origin(supports_credentials=True)
def check_username():
    username = request.args.get("username")

    exists = user_mgmt.user_exists(username)

    return jsonify({"exists": exists})


@app.route("/create-user", methods=["POST"])
@cross_origin(supports_credentials=True)
def make_user():

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    user_mgmt.create_user(
        data["username"], data["email_address"], data["hashed_password"]
    )

    return jsonify({"message": "Successfully created user!"}), 200


@app.route("/get-cars", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_users_cars():
    user_id = request.args.get("user_id", type=int)

    cars = car_mgmt.get_cars(user_id)

    return jsonify({"cars": cars})


@app.route("/get-models", methods=["GET"])
@cross_origin(supports_credentials=True)
def get_car_models():

    search_term = request.args.get("search_term")

    car_models = car_mgmt.get_models(search_term)

    return jsonify({"car_models": car_models})


@app.route("/search-cars", methods=["GET"])
@cross_origin(supports_credentials=True)
def search_car():

    search_term = request.args.get("search_term")
    cars = car_mgmt.find_cars(search_term)

    return jsonify({"cars": cars})


@app.route("/register-car", methods=["POST"])
@cross_origin(supports_credentials=True)
def register_car():

    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400

    data = request.get_json()

    success = car_mgmt.register(int(data["user_id"]), int(data["car_id"]))

    if success:
        return jsonify({"message": "Successfully created user!"}), 200

    return jsonify({"error": "User already registered this car!"}), 400


if __name__ == "__main__":
    app.run(debug=True)

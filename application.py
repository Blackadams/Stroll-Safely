from flask import Flask, render_template, jsonify, request
from model import connect_to_db

from middle import address_to_lat_lng, execute_waypoint_sequence
from middle import total_crimes_in_bounds
import json

app = Flask(__name__)


@app.route('/')
def index():
    """ runs app name mainspace """
    return render_template("main.html")


@app.route('/start-end.json')
def parse_user_start_end():
    """ takes the user's start and end points in address form
        and convert to latitude, longitude """

    # retrieve parameters and get their data from the /start-end.json endpoint
    start = request.args.get('start')
    end = request.args.get('end')

    # assemble a dictionary to push into the address_to_lat_lng() function
    start_end_dict = {'start': start, 'end': end}

    # returns latitude and longitude of point A and point B
    lat_lng_dict = address_to_lat_lng(start_end_dict)

    return jsonify(lat_lng_dict)


@app.route('/directions-data.json', methods=['POST'])
def directionsData():
    """ This holds all of the leg information pertaining to the route
        and all of this other fancy stuff  and returns back the waypoint(s)
        if necessary. """

    # this section is a workaround based on issues noted in deployment (HTTP 414 error)
    # directions_data = request.args.get('data')
    directions_data_key = request.form.keys()
    directions_data_value = request.form.values()
    directions_data = directions_data_key[0] + directions_data_value[0]
    directions_data = json.loads(directions_data)

    # print "+++++++++++++++++++++++++++++++++++++++++++++"
    # print "This is directions_data type", type(directions_data)
    # print "This is directions_data", json.dumps(directions_data, indent=2)
    # print "+++++++++++++++++++++++++++++++++++++++++++++"

    # call a function in middle.py that takes the directions and manipulates
    waypoints = execute_waypoint_sequence(directions_data)

    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    print "THIS IS WAYPOINTS", waypoints  # currently is a list of locations [{location: ...}, {location: ...}]
    print "This is directions_data type", type(waypoints)  # type list
    print "This is directions_data, json.dumps type", type(json.dumps(waypoints))  # type string
    print "Is this a string type for real?", isinstance(json.dumps(waypoints), str)  # true
    print "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"
    # waypoints to be sent back, json.dumps because we're sending a list
    # return json.dumps(waypoints)
    if waypoints is None:
        waypoints = []
    return jsonify(waypoints)


@app.route('/crimes.json')
def crimes():
    """ return a json of crimes lat, longitude """
    # crimes_coords = {'crimes': [
    #         {'latitude': 40.7127837, 'longitude': -74.00594130000002},
    #         {'latitude': 40.57948579, 'longitude': -73.99844033},
    #         {'latitude': 40.83069115, 'longitude': -73.95586724}
    #         ]}
    # crimes_coords = get_twenty()
    # return jsonify(crimes_coords)
    start_lat = request.args.get('start_lat')
    start_lng = request.args.get('start_lng')

    end_lat = request.args.get('end_lat')
    end_lng = request.args.get('end_lng')

    start_end_dict = {'point_a': {
                      'lat': float(start_lat),
                      'lng': float(start_lng)},
                      'point_b': {
                          'lat': float(end_lat),
                          'lng': float(end_lng)}}

    crimes_coords = total_crimes_in_bounds(start_end_dict)
    return jsonify(crimes_coords)

if __name__ == '__main__':
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    connect_to_db(app)
    app.run(debug=True)

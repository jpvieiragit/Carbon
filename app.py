#!flask/bin/python
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)
    
@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/carbon/api/v1.0/house/electricity', methods=['GET'])
@auth.login_required
def calculate_electricity():
    """
    Household carbon footprint calculator
    Enter your consumption of each type of energy
    ---
    tags:
      - House
    parameters:
      - name: method
        in: R$/mês=1, kWh/mês=2
        type: integer
        required: true
        description: type of energy
      - name: consume
        type: integer
        description: consume
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer
    """
    if not request.json or not 'method' in request.json:
        abort(400)

    method = request.json['method']
    consume = request.json.get('consume', 1)

    CONSUME_TYPE = {
        'RS': 1,
        'kWh': 2,
    }

    if method == CONSUME_TYPE['RS']:
        factor = 0.005
    if method == CONSUME_TYPE['kWh']:
        factor = 0.002

    result = consume * factor

    return jsonify({'result': r}), 201

@app.route('/carbon/api/v1.0/house/gas', methods=['GET'])
@auth.login_required
def calculate_gas():
    """
    Household carbon footprint calculator
    Enter your consumption of each type of energy
    ---
    tags:
      - House
    parameters:
      - name: method
        in: R$/mês=1, m³/mês=2, Botijão/ano=3
        type: integer
        required: true
        description: type of gás
      - name: consume
        type: integer
        description: consume
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer

    """
    if not request.json or not 'method' in request.json:
        abort(400)

    method = request.json['method']
    consume = request.json.get('consume', 1)

    CONSUME_TYPE = {
        'RS': 1,
        'M3': 2,
        'LPG':3,
    }

    if method == CONSUME_TYPE['RS']:
        factor = 0.01
    if method == CONSUME_TYPE['M3']:
        factor = 0.02
    if method == CONSUME_TYPE['LPG']:
        factor = 0.15

    result = consume * factor

    return jsonify({'result': result}), 201

@app.route('/carbon/api/v1.0/transport/flight', methods=['GET'])
@auth.login_required
def calculate_flight():
    """
    Flight carbon footprint calculator
    Enter your consumption for distance
    ---
    tags:
      - Flight
    parameters:
      - name: distance
        type: integer
        description: consume per distance
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer

    """
    if not request.json or not 'distance' in request.json:
        abort(400)

    distance = request.json['distance']
    factor = 52.27

    result = distance * factor

    return jsonify({'result': result}), 201

@app.route('/carbon/api/v1.0/transport/public', methods=['GET'])
@auth.login_required
def calculate_public():
    """
    Public transport carbon footprint calculator
    Enter mileage for each type of public transport
    ---
    tags:
      - Transport
    parameters:
      - name: method
        in: Taxi=1, Bus=2, Subway=3, Train=4, Ferry=5
        type: integer
        required: true
        description: type of transport
      - name: consume
        type: integer
        description: consume
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer

    """
    if not request.json or not 'method' in request.json:
        abort(400)

    method = request.json['method']
    consume = request.json.get('consume', 1)
    
    CONSUME_TYPE = {
        'Taxi': 1,
        'Bus': 2,
        'Subway': 3,
        'Train': 4,
        'Ferry': 5,
    }

    if method == CONSUME_TYPE['Taxi']:
        factor = 1.1
    if method == CONSUME_TYPE['Bus']:
        factor = 0.98
    if method == CONSUME_TYPE['Subway']:
        factor = 0.76
    if method == CONSUME_TYPE['Train']:
        factor = 0.74
    if method == CONSUME_TYPE['Ferry']:
        factor = 0.23

    result = consume * factor

    return jsonify({'result': result}), 201

@app.route('/carbon/api/v1.0/transport/car', methods=['GET'])
@auth.login_required
def calculate_car():
    """
    Car carbon footprint calculator
    Enter mileage for each type of fuel
    ---
    tags:
      - Transport
    parameters:
      - name: method
        in: Gasoline=1, Diesel=2, GNV=3, Flex=4
        type: integer
        required: true
        description: type of fuel
      - name: consume
        type: integer
        description: consume
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer

    """
    if not request.json or not 'method' in request.json:
        abort(400)

    method = request.json['method']
    consume = request.json.get('consume', 1)

    CONSUME_TYPE = {
        'Gasoline': 1,
        'Diesel': 2,
        'GNV':3,
        'Flex':4,
    }

    if method == CONSUME_TYPE['Gasoline']:
        factor = 1.74
    if method == CONSUME_TYPE['Diesel']:
        factor = 2.82
    if method == CONSUME_TYPE['GNV']:
        factor = 1.65
    if method == CONSUME_TYPE['Flex']:
        factor = 0.87

    result = consume * factor

    return jsonify({'result': result}), 201

@app.route('/carbon/api/v1.0/transport/motorbike', methods=['GET'])
@auth.login_required
def calculate_motorbike():
    """
    Motorbike carbon footprint calculator
    Enter mileage for each type of fuel
    ---
    tags:
      - Transport
    parameters:
      - name: method
        in: Gasoline=1, Etanol=2
        type: integer
        required: true
        description: type of fuel
      - name: motor
        type: integer
        description: range motor
      - name: consume
        type: integer
        description: Consume
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer

    """
    if not request.json:
        abort(400)
    if not 'method' in request.json:
        abort(400)
    if not 'motor' in request.json:
        abort(400)

    method = request.json['method']
    motor = request.json['motor']
    consume = request.json.get('consume', 1)

    CONSUME_TYPE = {
        'Gasoline': 1,
        'Etanol': 2,
    }

    if method == CONSUME_TYPE['Gasoline']:
        if motor == 150:
            factor = 0.68
        elif motor in range(150, 250, 1):
            factor = 0.78
        elif motor in range(250, 350, 1):
            factor = 0.85
        elif motor in range(350, 450, 1):
            factor = 0.97
        elif motor in range(450, 600, 1):
            factor = 1.24
        else:
            factor = 1.6
    if method == CONSUME_TYPE['Etanol']:
        if motor == 150:
            factor = 0.34
        elif motor in range(150, 250, 1):
            factor = 0.39
        elif motor in range(250, 350, 1):
            factor = 0.43
        elif motor in range(350, 450, 1):
            factor = 0.49
        elif motor in range(450, 600, 1):
            factor = 0.62
        else:
            factor = 0.8

    result = consume * factor

    return jsonify({'result': result}), 201

@app.route('/carbon/api/v1.0/food', methods=['GET'])
@auth.login_required
def calculate_food():
    """
    Household carbon footprint calculator
    Enter your consumption of each type of food
    ---
    tags:
      - House
    parameters:
      - name: consume
        type: array
        in: (1, 1, 1), (2, 2, 2), (2, 2, 3), (2, 3, 2), (3, 2, 2), (0, 0, 0)
        description: often consume food [meat, chicken, pork]
    responses:
      400:
        description: Bad request
      401:
        description: Unauthorized access
      404:
        description: Not found
      200:
        description: Response (Kg)
        schema:
          properties:
            factor:
              type: integer

    """
    if not request.json or not 'consume' in request.json:
        abort(400)

    consume = request.json['consume']

    if consume == [1, 1, 1]:
        factor = 0.08
    elif consume == [2, 2, 2]:
        factor = 0.31
    elif consume == [2, 2, 3]:
        factor = 0.24
    elif consume == [2, 3, 2]:
        factor = 0.17
    elif consume == [3, 2, 2]:
        factor = 0.54
    else:
        factor = 0.0

    result = factor

    return jsonify({'result': result}), 201

if __name__ == '__main__':
    app.run(debug=True)
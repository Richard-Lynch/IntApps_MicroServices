#!/usr/local/bin/python3

from flask import Flask, jsonify, request, make_response, abort
app = Flask(__name__)

pals = [
        {"name": "Richie", 'id' : 0},
        {"name": "Ali", 'id' : 1},
        {"name": "Jenny", 'id' : 2},
        {"name": "Ste", 'id' : 3}
        ]

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/', methods=['GET'])
def root():
    return jsonify({'test' : 'success!'})

@app.route('/pals', methods=['GET'])
def get_pals():
    return jsonify({'pals' : pals})

@app.route('/pals/<string:name>', methods=['GET'])
def get_pal(name):
    pal_list = [ p for p in pals if p['name'] == name ] 
    if len(pal_list) == 0:
        abort(404)
    return jsonify({'pal' : pal_list[0]})

@app.route('/pals', methods=['POST'])
def create_pal():
    if not request.json or not 'name' in request.json:
        print ("json:", request.json)
        abort(400)
    p = {
            'id' : pals[-1]['id'] + 1,
            'name' : request.json['name']
            }
    pals.append(p)
    return jsonify({'pal' : p}), 201

@app.route('/pals/<int:pal_id>', methods=['PUT'])
def update_pal(pal_id):
    pal_list = [ p for p in pals if p['id'] == pal_id ] 
    if len(pal_list) == 0:
        print ("zero len")
        abort(404)
    if not request.json:
        print ("not json")
        abort(400)
    if 'name' in request.json and type(request.json['name']) is not str:
        print ("json:", request.json)
        print ("type:", type(request.json))
        print ("type:", type(request.json['name']))
        print ("no name")
        abort(400)
    pal_list[0]['name'] = request.json.get('name', pal_list[0]['name']) # deal with name being empty (for multiple values), default to old value
    return jsonify({'pal' : pal_list[0]})

@app.route('/pals/<int:pal_id>', methods=['DELETE'])
def delete_pal(pal_id):
    pal_list = [ p for p in pals if p['id'] == pal_id ] 
    if len(pal_list) == 0:
        abort(404)
    pals.remove(pal_list[0])
    return jsonify({'result' : True})
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)


# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import sys
import logging
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
port = int(sys.argv[1])
path_config = sys.argv[2]
with open(path_config,'r') as f:
    config = json.load(f)
w = config['weight_w']
config['weight_w'] = [float(w[i]) for i in range(len(w))]
config['weight_b'] = float(config['weight_b'])
config['threshold'] = 0.8
@app.route('/api/modelconfig', methods=['get'])
def test2():
    try:
        response = config
        response['message'] = 'sucess'
    except Exception as e:
        app.logger.error("error:",e)
        response = {'message': 'error'}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)

# -*- encoding: utf-8 -*-
from flask import Flask, request, Response
import json
import sys
from datetime import datetime
import time
import logging
from Config import config_predict,Config_train,getConfig_feature
from modelpredict import getModel,predicting
app = Flask(__name__)
app.logger.setLevel(logging.INFO)
port = 5000
style = 0#0大白狗, 1散文
if len(sys.argv)>1:
   port = int(sys.argv[1])
ConfigPredict = config_predict()
ConfigTrain = Config_train()
ConfigFeature= getConfig_feature(ConfigPredict)
X_holder, y_holder, learning_rate, predict_y, loss, optimizer, train_op, grads, accuracy,session = getModel(ConfigTrain,ConfigPredict)
@app.route('/api/gen', methods=['POST'])
def test2():
    r = request.json
    data = r["input"]
    try:
        p = 0.0
        result = 0
        p,result = predicting(data, ConfigFeature, X_holder, y_holder, learning_rate, predict_y, session, thr=ConfigPredict.thr)
        p = '%0.4f'%p
        result = str(result)
        app.logger.info("input:{}".format(data))
        app.logger.info("output:\n{}".format('\n'.join(result)))
        response = {'message':'success','input':data,'result': result,'prob':p}
    except Exception as e:
        app.logger.error("error:",e)
        response = {'message': 'error', 'input': data, 'result': None}
    response_pickled = json.dumps(response)
    return Response(response=response_pickled, status=200, mimetype="application/json")

# start flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=port)

# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements. See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License. You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, jsonify, request
import pandas as pd
from sklearn.externals import joblib
import traceback
from waitress import serve

app = Flask(__name__)
model = None
model_columns = None

'''
Example :
curl -d '[{"pickup_community_area":32.0,"fare":5.05,"trip_start_month":5.0,"trip_start_hour":13.0,
"trip_start_day":2.0,"trip_start_timestamp":1431954900.0,
"pickup_latitude":41.880994471,"pickup_longitude":
-87.632746489,"dropoff_latitude":41.879255084,"dropoff_longitude":-87.642648998,"trip_miles":0.0,
"pickup_census_tract":0.0,"dropoff_census_tract":17031281900.0,
"payment_type":0.0,"company":60.0,"trip_seconds":30.0,
"dropoff_community_area":30.0}]' -H "Content-Type: application/json" \
-X POST http://0.0.0.0:8080/predict && \
echo -e "\n -> predict OK"
'''


@app.route('/predict', methods=['POST'])
def predict():
    try:
        json_ = request.json
        query_df = pd.DataFrame(json_)
        query = pd.get_dummies(query_df)
        query = query.reindex(columns=model_columns, fill_value=0)
        prediction = model.predict(query)
        return jsonify({"prediction": list(map(int, prediction))})
    except Exception as e:  # pylint: disable=broad-except
        return jsonify({'error': str(e), 'trace': traceback.format_exc()})


@app.route("/", methods=['GET'])
def root():
    return "Use http://localhost:8080/predict? to predict"


def pickle(model_file_name, model_columns_file_name):
    global model, model_columns
    model = joblib.load(model_file_name)
    model_columns = joblib.load(model_columns_file_name)
    # app.run(port=8080, debug=True)
    serve(app, host='0.0.0.0', port=8080)

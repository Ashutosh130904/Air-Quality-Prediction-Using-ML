from flask import Flask, request, jsonify
import numpy as np
import joblib 
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  

model = joblib.load('air_quality_prediction.pkl')  

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

   
    features = [
        float(data['pm25']),
        float(data['pm10']),
        float(data['no2']),
        float(data['nh3']),
        float(data['so2']),
        float(data['co']),
        float(data['ozone']),
    ]

    # Reshape for prediction
    input_data = np.array([features])
  
    prediction = model.predict(input_data)

    result = str(prediction[0])

    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)

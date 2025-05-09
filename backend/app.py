from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import logging
import os

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model_pipeline.pkl')
try:
    model = joblib.load(MODEL_PATH)
    logger.info("Model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading model: {str(e)}")
    raise

@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Check if model is loaded
        if model is not None:
            return jsonify({'status': 'healthy', 'message': 'Model is loaded and service is running'}), 200
        else:
            return jsonify({'status': 'unhealthy', 'message': 'Model is not loaded'}), 500
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'message': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        logger.info(f"Received data: {data}")

        expected_fields = [
            'age', 'sex', 'cp', 'trtbps', 'chol', 'fbs', 'restecg',
            'thalachh', 'exng', 'oldpeak', 'slp', 'caa', 'thall'
        ]

        if not all(field in data for field in expected_fields):
            missing = [field for field in expected_fields if field not in data]
            return jsonify({'status': 'failed', 'error': f'Missing fields: {missing}'}), 400

        # Convert input data to appropriate types
        df = pd.DataFrame([{
            'age': int(data['age']),
            'sex': int(data['sex']),
            'cp': int(data['cp']),
            'trtbps': float(data['trtbps']),
            'chol': float(data['chol']),
            'fbs': int(data['fbs']),
            'restecg': int(data['restecg']),
            'thalachh': float(data['thalachh']),
            'exng': int(data['exng']),
            'oldpeak': float(data['oldpeak']),
            'slp': int(data['slp']),
            'caa': int(data['caa']),
            'thall': int(data['thall']),
        }])

        prediction = model.predict(df)
        result = int(prediction[0])
        logger.info(f"Prediction result: {result}")

        return jsonify({'prediction': result, 'status': 'success'})

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'status': 'failed', 'error': str(e)}), 400

if __name__ == '__main__':
    # In production, use gunicorn or similar WSGI server
    app.run(host='0.0.0.0', port=5000)

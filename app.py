from flask import Flask, request, jsonify, render_template
from flask_firebase import FirebaseAuth
from geospatial.sentinel_api import fetch_satellite_data
import tensorflow as tf

app = Flask(__name__)
app.config['FIREBASE_AUTH'] = {
    'certificate': 'path/to/firebase-cert.json'
}
auth = FirebaseAuth(app)

# Load model
model = tf.keras.models.load_model('plant_model.h5')

@app.route('/')
@auth.required
def home():
    return render_template('map.html')

@app.route('/predict', methods=['GET', 'POST'])
@auth.required
def predict():
    # Image prediction logic (from previous snippet)
    ...

@app.route('/map', methods=['GET'])
@auth.required
def map_view():
    return render_template('map.html')

@app.route('/map-data', methods=['GET'])
def get_map_data():
    """Endpoint to fetch satellite data for given coordinates"""
    try:
        latitude = request.args.get('lat')
        longitude = request.args.get('lng')
        if not latitude or not longitude:
            return jsonify({'error': 'Missing lat/lng parameters'}), 400
        
        satellite_data = fetch_satellite_data(latitude, longitude)
        if 'error' in satellite_data:
            return jsonify(satellite_data), 500
            
        return jsonify(satellite_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)